import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username


# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# Message model
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # Automatically set timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # New field to track message creation time

    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:20]}"
