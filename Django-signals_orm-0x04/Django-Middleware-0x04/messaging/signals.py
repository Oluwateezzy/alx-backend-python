# chats/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=get_user_model())
def cleanup_user_messaging_data(sender, instance, **kwargs):
    """
    Clean up all messaging-related data when a user is deleted:
    - Messages where user was sender or receiver
    - Notifications related to those messages
    - Message history records
    - Conversations where user was the only participant
    """
    # Delete all messages where user was either sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for this user
    Notification.objects.filter(user=instance).delete()
    
    # Clean up message history for deleted messages
    # (This would be handled automatically by CASCADE, but we do it explicitly)
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
    
    # Clean up conversations where this was the last participant
    for conversation in instance.conversations.all():
        if conversation.participants.count() <= 1:
            conversation.delete()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created and instance.receiver:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=old_instance,
            content=old_instance.content,
        )
        instance.edited = True 