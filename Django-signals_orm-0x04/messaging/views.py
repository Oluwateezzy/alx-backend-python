
from django.dispatch import receiver
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .pagination import MessageResultsSetPagination
from .permission import IsParticipantOfConversation
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    
    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if not participants or not isinstance(participants, list):
            return Response({"error": "Participants list is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Add requesting user if not included
        user_id = request.user.user_id
        if user_id not in participants:
            participants.append(user_id)

        # Validate that all participants exist
        User = get_user_model()
        valid_users = User.objects.filter(user_id__in=participants).values_list('user_id', flat=True)
        if set(participants) != set(valid_users):
            return Response({"error": "One or more participant IDs are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if conversation with same participants already exists
        existing_conversations = Conversation.objects.all()
        for conv in existing_conversations:
            conv_participants = set(conv.participants.values_list('user_id', flat=True))
            if conv_participants == set(participants):
                serializer = self.get_serializer(conv)
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    pagination_class = MessageResultsSetPagination
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        Edit a message.
        Only the sender of the message can edit it.
        The 'content' field must be provided.
        """
        message = self.get_object()

        if message.sender != request.user:
            return Response({"detail": "You can only edit your own messages."},
                            status=status.HTTP_403_FORBIDDEN)

        new_content = request.data.get("content")
        if not new_content:
            return Response({"error": "Content is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        message.content = new_content
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Requires 'conversation' (conversation_id) and 'content' in request data.
        The sender is set to the logged-in user.
        """
        conversation_id = request.data.get('conversation')
        content = request.data.get('content')

        if not conversation_id or not content:
            return Response({"error": "Both conversation and content are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."},
                            status=status.HTTP_404_NOT_FOUND)

        
        participants = conversation.participants.all()
        receiver = [user for user in participants if user != request.user]
        receiver = receiver[0] if receiver else None  # Fallback to avoid index error

        if not receiver:
            return Response({"error": "Receiver could not be determined."},
                            status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            conversation=conversation,
            content=content
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Function-based view to allow authenticated users to delete their account.
    Automatically deletes related messages and conversations.
    """
    user = request.user

    # Optional confirmation step (uncomment to use)
    # if not request.data.get('confirm'):
    #     return Response(
    #         {"error": "Confirmation required. Send 'confirm': true in request body"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    user_conversations = user.conversations.all()
    
    # Delete the user (triggers post_delete signal)
    user.delete()

    # Clean up any empty conversations
    for conversation in user_conversations:
        if conversation.participants.count() == 0:
            conversation.delete()

    return Response(
        {"detail": "Account and all related data deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )
    
class DeleteAccountView(viewsets.APIView):
    """
    API endpoint for users to delete their own account.
    Automatically cleans up related messages and conversations.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        
        # Optional confirmation step (uncomment to use)
        # if not request.data.get('confirm'):
        #     return Response(
        #         {"error": "Confirmation required. Send 'confirm': true in request body"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        # Get all conversations the user is part of before deletion
        user_conversations = user.conversations.all()
        
        # Delete the user (this will trigger our post_delete signal)
        user.delete()
        
        # Clean up empty conversations
        for conversation in user_conversations:
            if conversation.participants.count() == 0:
                conversation.delete()
        
        return Response(
            {"detail": "Account and all related data deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

@receiver(post_delete, sender=get_user_model())
def cleanup_user_messages(sender, instance, **kwargs):
    """
    Signal handler to clean up messaging data when a user is deleted.
    Handles:
    - Messages where user was sender
    - Messages where user was receiver
    - Conversations where user was the only participant
    """
    # Delete all messages where user was sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Clean up conversations where user was the only participant
    for conversation in instance.conversations.all():
        if conversation.participants.count() <= 1:
            conversation.delete()