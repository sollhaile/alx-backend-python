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