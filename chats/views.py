<<<<<<< HEAD
from rest_framework import viewsets
from .models import Chat, Message  # Make sure these models exist
from .serializers import ChatSerializer, MessageSerializer  # You'll need to create these

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(chat_id=self.kwargs['chat_pk'])
=======
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
from django.views.decorators.cache import cache_page

# Assuming you have a view like this:
@cache_page(60)  # Cache for 60 seconds
def conversation_messages(request, conversation_id):
    # Your existing code to get messages in the conversation
    # ...
    return render(request, 'conversation.html', context)
>>>>>>> 471d053 (messaging_app Dockerfile)
