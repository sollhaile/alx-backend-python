from rest_framework import serializers
<<<<<<< HEAD
=======
<<<<<<< HEAD
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
=======
>>>>>>> 693a14b50ad20d90e157c6d77f006ca46103a5a0
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()  # explicitly declare CharField

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()  # nested messages field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        # Example validation raising ValidationError
        if not data.get('participants'):
            raise serializers.ValidationError("At least one participant required")
        return data
<<<<<<< HEAD
=======
>>>>>>> 471d053 (messaging_app Dockerfile)
>>>>>>> 693a14b50ad20d90e157c6d77f006ca46103a5a0
