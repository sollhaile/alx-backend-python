from rest_framework import serializers
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
