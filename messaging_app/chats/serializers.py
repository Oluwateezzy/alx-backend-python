from rest_framework import serializers
from models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'phone_number',
            'profile_picture',
            'status',
            'last_online'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'read',
            'read_at',
            'attachment',
            'attachment_type'
        ]
        read_only_fields = ['sender', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    group_admin = UserSerializer(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'updated_at',
            'is_group',
            'group_name',
            'group_admin',
            'messages'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=True
    )
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'is_group',
            'group_name',
            'group_admin'
        ]

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'message_body',
            'attachment',
            'attachment_type'
        ]
        extra_kwargs = {
            'conversation': {'required': True}
        }