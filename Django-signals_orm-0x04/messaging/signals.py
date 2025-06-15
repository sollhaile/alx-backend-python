from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(user=instance).delete()
from django.db.models.signals import pre_save
from django.dispatch import receiver
from messaging.models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_old_message_content(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(   # ✅ this line is REQUIRED
                    message=old_instance,
                    old_content=old_instance.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

