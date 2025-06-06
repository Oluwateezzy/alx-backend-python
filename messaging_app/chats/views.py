from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from .permissions import IsOwnerOrParticipant

class ConversationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]  # Add JWT authentication
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]  # Add custom permission
    queryset = Conversation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['is_group', 'participants']
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ['group_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only show conversations where current user is a participant
        queryset = self.queryset.filter(participants=self.request.user)
        
        # Apply additional filtering
        is_group = self.request.query_params.get('is_group', None)
        if is_group is not None:
            queryset = queryset.filter(is_group=is_group.lower() == 'true')
            
        return queryset

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]
    queryset = Message.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['conversation', 'sender', 'read']
    ordering_fields = ['sent_at', 'read_at']
    search_fields = ['message_body']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        # Only show messages from conversations the user is in
        queryset = self.queryset.filter(
            conversation__participants=self.request.user
        ).order_by('-sent_at')
        
        # Apply additional filtering
        conversation_id = self.request.query_params.get('conversation', None)
        if conversation_id is not None:
            queryset = queryset.filter(conversation_id=conversation_id)
            
        read_status = self.request.query_params.get('read', None)
        if read_status is not None:
            queryset = queryset.filter(read=read_status.lower() == 'true')
            
        return queryset

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