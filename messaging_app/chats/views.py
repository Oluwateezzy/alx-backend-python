from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only show conversations where current user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Add current user to participants if not already included
        participants = list(serializer.validated_data['participants'])
        if request.user not in participants:
            participants.append(request.user)
        
        conversation = Conversation.objects.create(
            is_group=serializer.validated_data.get('is_group', False),
            group_name=serializer.validated_data.get('group_name'),
            group_admin=serializer.validated_data.get('group_admin')
        )
        conversation.participants.set(participants)
        
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        # Only show messages from conversations the user is in
        return self.queryset.filter(
            conversation__participants=self.request.user
        ).order_by('-sent_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify user is in the conversation
        conversation = serializer.validated_data['conversation']
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=serializer.validated_data.get('message_body'),
            attachment=serializer.validated_data.get('attachment'),
            attachment_type=serializer.validated_data.get('attachment_type')
        )
        
        # Update conversation's updated_at timestamp
        conversation.save()
        
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )