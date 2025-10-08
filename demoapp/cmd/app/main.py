import os
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
from prometheus_client import generate_latest, REGISTRY

# Allow running this file directly by ensuring the project root is on sys.path
import os as _os
import sys as _sys
if __package__ is None or __package__ == "":
    _PROJECT_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "../../.."))
    if _PROJECT_ROOT not in _sys.path:
        _sys.path.insert(0, _PROJECT_ROOT)

from demoapp.internal.metrics import metrics
from demoapp.internal.middleware.httpmetrics import http_metrics_middleware, get_route_pattern
from demoapp.internal.middleware.inflightrequest import inflight_requests_middleware

class StatusResponseWriter:
    def __init__(self, handler):
        self.handler = handler
        self.status = 200
    
    def write_header(self, status: int):
        self.status = status
        self.handler.send_response(status)
    
    def get_status_string(self) -> str:
        return str(self.status)

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self._response_status = 200
        super().__init__(*args, **kwargs)
    
    def send_response(self, code, message=None):
        self._response_status = code
        super().send_response(code, message)
    
    def get_status_string(self):
        return str(self._response_status)
    
    def get_route_pattern(self):
        return get_route_pattern(self)
    
    @http_metrics_middleware
    @inflight_requests_middleware
    def do_GET(self):
        """
        Обработчик GET запросов с примененными middleware
        """
        try:
            # Создаем StatusResponseWriter
            status_writer = StatusResponseWriter(self)
            
            # Парсим URL
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            # Логируем запрос
            self.log_message(f"GET {path}")
            
            # Обрабатываем различные эндпоинты
            if path == "/code-2xx":
                status = self.random_2xx()
                status_writer.write_header(status)
                self.end_headers()
                
            elif path == "/code-4xx":
                status = self.random_4xx()
                status_writer.write_header(status)
                self.end_headers()
                
            elif path == "/code-5xx":
                status = self.random_5xx()
                status_writer.write_header(status)
                self.end_headers()
                
            elif path == "/ms-200":
                sleep_time = self.random_duration_ms(200) / 1000.0
                time.sleep(sleep_time)
                status_writer.write_header(200)
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                
            elif path == "/ms-500":
                sleep_time = self.random_duration_ms(500) / 1000.0
                time.sleep(sleep_time)
                status_writer.write_header(200)
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                
            elif path == "/ms-1000":
                sleep_time = self.random_duration_ms(1000) / 1000.0
                time.sleep(sleep_time)
                status_writer.write_header(200)
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                
            elif path == "/metrics":
                status_writer.write_header(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(generate_latest(REGISTRY))
                
            else:
                status_writer.write_header(404)
                self.end_headers()
            
        except Exception as e:
            self.log_error(f"Error handling request: {e}")
            self.send_response(500)
            self.end_headers()
    
    def random_2xx(self):
        return random.choice([200, 201, 202, 204])
    
    def random_4xx(self):
        return random.choice([400, 401, 403, 404, 409, 422, 429])
    
    def random_5xx(self):
        return random.choice([500, 502, 503, 504])
    
    def random_duration_ms(self, max_ms):
        return random.uniform(0, max_ms)
    
    def log_message(self, format, *args):
        print(f"{self.log_date_time_string()} - {format % args}")
    
    def log_error(self, message):
        print(f"ERROR: {message}")

def get_http_requests_inflight_max():
    http_requests_inflight_max_string = os.getenv("HTTP_REQUESTS_INFLIGHT_MAX")
    http_requests_inflight_max = 20.0
    
    if http_requests_inflight_max_string:
        try:
            http_requests_inflight_max = float(http_requests_inflight_max_string)
        except (ValueError, TypeError):
            pass
    
    return http_requests_inflight_max

def main():
    # Устанавливаем максимальное количество inflight запросов
    max_inflight = get_http_requests_inflight_max()
    metrics.HttpRequestsInflightMax.set(max_inflight)
    
    server = HTTPServer(('0.0.0.0', 8080), RequestHandler)
    print("Starting server on http://0.0.0.0:8080")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    main()
