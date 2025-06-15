import datetime

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
