#!/usr/bin/env python3

import os
import time
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from internal.helpers.http import Random2xx, Random4xx, Random5xx, RandomDurationMS
from internal.metrics.metrics import (
    http_requests_inflight_max,
    http_requests_total,
    http_requests_current,
    http_requests_duration_histogram,
    http_requests_duration_summary,
    register_metrics
)


def get_http_requests_inflight_max():
    """Get max inflight requests from environment variable."""
    http_requests_inflight_max_str = os.getenv("HTTP_REQUESTS_INFLIGHT_MAX", "20.0")
    try:
        return float(http_requests_inflight_max_str)
    except ValueError:
        return 20.0


class DemoHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the demo application."""
    
    def do_GET(self):
        """Handle GET requests."""
        start_time = time.time()
        
        # Increment inflight requests
        http_requests_current.inc()
        
        try:
            # Parse the URL
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            # Route the request
            if path == '/code-2xx':
                self._handle_code_2xx()
            elif path == '/code-4xx':
                self._handle_code_4xx()
            elif path == '/code-5xx':
                self._handle_code_5xx()
            elif path == '/ms-200':
                self._handle_ms_200()
            elif path == '/ms-500':
                self._handle_ms_500()
            elif path == '/ms-1000':
                self._handle_ms_1000()
            elif path == '/metrics':
                self._handle_metrics()
            else:
                self._handle_not_found()
            
            # Record metrics
            elapsed_seconds = time.time() - start_time
            status_code = getattr(self, '_status_code', 200)
            
            http_requests_total.labels(
                pattern=path,
                method=self.command,
                status=str(status_code)
            ).inc()
            
            http_requests_duration_histogram.labels(
                pattern=path,
                method=self.command
            ).observe(elapsed_seconds)
            
            http_requests_duration_summary.labels(
                pattern=path,
                method=self.command
            ).observe(elapsed_seconds)
            
        finally:
            # Decrement inflight requests
            http_requests_current.dec()
    
    def _handle_code_2xx(self):
        """Handle /code-2xx endpoint."""
        status_code = Random2xx()
        self._status_code = status_code
        self.send_response(status_code)
        self.end_headers()
    
    def _handle_code_4xx(self):
        """Handle /code-4xx endpoint."""
        status_code = Random4xx()
        self._status_code = status_code
        self.send_response(status_code)
        self.end_headers()
    
    def _handle_code_5xx(self):
        """Handle /code-5xx endpoint."""
        status_code = Random5xx()
        self._status_code = status_code
        self.send_response(status_code)
        self.end_headers()
    
    def _handle_ms_200(self):
        """Handle /ms-200 endpoint."""
        duration = RandomDurationMS(200)
        time.sleep(duration)
        self._status_code = 200
        self.send_response(200)
        self.end_headers()
    
    def _handle_ms_500(self):
        """Handle /ms-500 endpoint."""
        duration = RandomDurationMS(500)
        time.sleep(duration)
        self._status_code = 200
        self.send_response(200)
        self.end_headers()
    
    def _handle_ms_1000(self):
        """Handle /ms-1000 endpoint."""
        duration = RandomDurationMS(1000)
        time.sleep(duration)
        self._status_code = 200
        self.send_response(200)
        self.end_headers()
    
    def _handle_metrics(self):
        """Handle /metrics endpoint."""
        metrics_data = generate_latest()
        self._status_code = 200
        self.send_response(200)
        self.send_header('Content-Type', CONTENT_TYPE_LATEST)
        self.send_header('Content-Length', str(len(metrics_data)))
        self.end_headers()
        self.wfile.write(metrics_data)
    
    def _handle_not_found(self):
        """Handle 404 Not Found."""
        self._status_code = 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """Log an arbitrary message."""
        print(f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}")


def main():
    """Main entry point."""
    # Register Prometheus metrics
    register_metrics()
    
    # Set max inflight requests
    max_inflight = get_http_requests_inflight_max()
    http_requests_inflight_max.set(max_inflight)
    
    # Create and start the HTTP server
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, DemoHTTPRequestHandler)
    
    print(f"Starting server on http://{server_address[0]}:{server_address[1]}")
    print("Available endpoints:")
    print("  GET /code-2xx   - Random 2xx status code")
    print("  GET /code-4xx   - Random 4xx status code") 
    print("  GET /code-5xx   - Random 5xx status code")
    print("  GET /ms-200     - Sleep up to 200ms")
    print("  GET /ms-500     - Sleep up to 500ms")
    print("  GET /ms-1000    - Sleep up to 1000ms")
    print("  GET /metrics    - Prometheus metrics")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    main()



