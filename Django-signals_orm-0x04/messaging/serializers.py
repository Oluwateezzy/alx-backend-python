from rest_framework import serializers
from .models import User, Conversation, Message
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    status = serializers.CharField(max_length=100, required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'user_id', 
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'full_name',
            'phone_number',
            'profile_picture',
            'status',
            'last_online'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=5000)
    attachment_type = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True
    )

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

    def validate(self, data):
        if not data.get('message_body') and not data.get('attachment'):
            raise serializers.ValidationError(
                "Either message_body or attachment must be provided"
            )
        return data

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    group_admin = UserSerializer(read_only=True)
    group_name = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_null=True
    )

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

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('-sent_at')[:100]  # Limit to 100 most recent
        return MessageSerializer(messages, many=True).data

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

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants"
            )
        return value

    def validate(self, data):
        if data.get('is_group') and not data.get('group_name'):
            raise serializers.ValidationError(
                "Group conversations must have a group name"
            )
        return data

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'message_body',
        ]