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