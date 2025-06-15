import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_line = f"{datetime.datetime.now()} - {request.method} {request.path}\n"
        with open("C:/Users/Y.S/Documents/alx-backend-python/Django-Middleware-0x03/requests.log", "a") as log_file:
            log_file.write(log_line)
        response = self.get_response(request)
        return response
