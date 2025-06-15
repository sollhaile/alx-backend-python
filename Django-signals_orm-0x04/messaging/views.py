from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({'message': 'User account deleted successfully'})
from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def message_thread_view(request):
    messages = Message.objects.filter(parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related('replies')
    return render(request, 'messaging/thread.html', {'messages': messages})
messages = Message.objects.filter(
    sender=request.user,
    receiver=some_receiver,  # make sure you define this
    parent_message__isnull=True
).select_related('sender', 'receiver').prefetch_related('replies')
def inbox(request):
    user = request.user
    # Use the custom manager's method, then chain .only() here explicitly:
    unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'read', 'created_at')
    return render(request, 'inbox.html', {'unread_messages': unread_messages})
from django.views.decorators.cache import cache_page

@cache_page(60)  # cache timeout of 60 seconds
def your_messages_view(request, conversation_id):
    # existing code to retrieve and render messages
    ...
