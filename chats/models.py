# chats/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add any additional fields here
    pass

class Chat(models.Model):
    # Your existing Chat model
    ...

class Message(models.Model):
    # Your existing Message model
    ...