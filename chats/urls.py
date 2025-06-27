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
