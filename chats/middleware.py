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
        log_entry = f"[{timestamp}] {ip} {method} {path} {user_agent}\n"

        # Write to file
        with open('requests.log', 'a') as log_file:
            log_file.write(log_entry)

        # Continue with the response
        return self.get_response(request)
# chats/middleware.py

import time

class ResponseTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        response["X-Response-Time"] = f"{duration:.4f}s"
        return response
