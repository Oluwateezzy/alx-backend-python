from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to:
    - Send messages to the conversation
    - View the conversation and its messages
    - Update/delete their own messages in the conversation
    """
    
    def has_permission(self, request, view):
        # First check if the user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # For list/create actions, check conversation ID in request data
        if view.action in ['list', 'create']:
            conversation_id = request.data.get('conversation') or request.query_params.get('conversation')
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(pk=conversation_id)
                    return request.user in conversation.participants.all()
                except Conversation.DoesNotExist:
                    return False
            return True  # Allow listing, but filter by participant in get_queryset
        
        return True  # For other actions, check object permission

    def has_object_permission(self, request, view, obj):
        # Handle Message objects
        if isinstance(obj, Message):
            # Allow read-only for participants
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return request.user in obj.conversation.participants.all()
            # Allow update/delete only for message owner
            elif request.method in ['PUT', 'PATCH', 'DELETE']:
                return obj.sender == request.user and request.user in obj.conversation.participants.all()
        
        # Handle Conversation objects
        elif isinstance(obj, Conversation):
            # Only participants can view the conversation
            return request.user in obj.participants.all()
        
        return False
