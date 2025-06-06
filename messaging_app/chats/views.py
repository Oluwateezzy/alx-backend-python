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
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
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
        # Let the permission class handle participant filtering
        queryset = super().get_queryset()
        
        # Apply additional query parameters
        is_group = self.request.query_params.get('is_group')
        if is_group is not None:
            queryset = queryset.filter(is_group=is_group.lower() == 'true')
            
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        
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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
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
        # Base queryset is filtered by permission class
        queryset = super().get_queryset().order_by('-sent_at')
        
        # Apply additional query parameters
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id is not None:
            queryset = queryset.filter(conversation_id=conversation_id)
            
        read_status = self.request.query_params.get('read')
        if read_status is not None:
            queryset = queryset.filter(read=read_status.lower() == 'true')
            
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        conversation = serializer.validated_data['conversation']
        
        # Permission class already checks if user is participant
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=serializer.validated_data.get('message_body'),
            attachment=serializer.validated_data.get('attachment'),
            attachment_type=serializer.validated_data.get('attachment_type')
        )
        
        conversation.save()  # Update conversation's updated_at
        
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )