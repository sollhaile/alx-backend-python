from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet


from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),  # <- This line is required
]
