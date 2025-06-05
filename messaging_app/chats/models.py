from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    last_online = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    

    def __str__(self):
        return self.username


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    group_admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_of_groups'
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('conversation')
        verbose_name_plural = _('conversations')
    
    def __str__(self):
        if self.is_group:
            return f"Group: {self.group_name}"
        participants = self.participants.all()
        return f"Chat between {participants[0]} and {participants[1]}" if len(participants) == 2 else f"Multi-user chat ({len(participants)} users)"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    
    # For media messages
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    attachment_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('image', 'Image'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('audio', 'Audio')
        ]
    )
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('message')
        verbose_name_plural = _('messages')
    
    def __str__(self):
        return f"Message from {self.sender} in {self.conversation} at {self.timestamp}"