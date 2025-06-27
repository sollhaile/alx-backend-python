import datetime
from django.http import HttpResponseForbidden

class RolepermissionMiddleware:  # 👈 lowercase "p" as required
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: You do not have permission.")
        else:
            return HttpResponseForbidden("Access denied: You must be logged in.")

        return self.get_response(request)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Gather info
        method = request.method
        path = request.get_full_path()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Format log line
        log_path = "C:/Users/Y.S/Documents/alx-backend-python/Django-Middleware-0x03/requests.log"
        
        # Write to file
        with open('requests.log', 'a') as log_file:
            log_file.write(log_path)

        # Continue with the response
        return self.get_response(request)
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()

        # Allowed between 6 PM (18:00) and 9 PM (21:00)
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to the chat is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)
import time
from collections import defaultdict
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)  # Stores list of timestamps per IP

    def __call__(self, request):
        # Only limit POST requests (typically used to send messages)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than 60 seconds
            self.request_log[ip] = [
                timestamp for timestamp in self.request_log[ip]
                if current_time - timestamp < 60
            ]

            # Check if IP exceeded 5 messages in last 60 seconds
            if len(self.request_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            # Add current timestamp
            self.request_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Get IP from headers or meta
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
