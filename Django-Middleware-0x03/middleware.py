import time
from django.utils.deprecation import MiddlewareMixin

class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        total_time = time.time() - getattr(request, 'start_time', time.time())
        log_line = (
            f"METHOD: {request.method} | "
            f"PATH: {request.get_full_path()} | "
            f"STATUS: {response.status_code} | "
            f"TIME: {total_time:.4f} seconds\n"
        )

        with open('requests.log', 'a') as log_file:
            log_file.write(log_line)
        return response
