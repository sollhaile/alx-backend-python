from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(user=instance).delete()
