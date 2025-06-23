<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import include, path
from . import views

# Create a parent router first
parent_router = DefaultRouter()

# Register parent routes
parent_router.register('chats', views.ChatViewSet, basename='chats')

# Then create nested routers
chat_router = routers.NestedDefaultRouter(parent_router, 'chats', lookup='chat')
chat_router.register('messages', views.MessageViewSet, basename='chat-messages')

urlpatterns = [
    # Include both parent and nested routes
    path('', include(parent_router.urls)),
    path('', include(chat_router.urls)),
]
=======
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

message_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
message_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(message_router.urls)),
]
>>>>>>> 471d053 (messaging_app Dockerfile)
