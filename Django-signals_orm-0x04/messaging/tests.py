from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class NotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")
        self.assertTrue(Notification.objects.filter(message=msg, user=self.receiver).exists())
