from http.server import BaseHTTPRequestHandler

class StatusTrackingHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self._response_status = 200
        super().__init__(*args, **kwargs)
    
    def send_response(self, code, message=None):
        self._response_status = code
        super().send_response(code, message)
    
    def get_status_string(self):
        return str(self._response_status)


class StatusResponseWriter:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self._handler = handler
        self._status = 200

    def write_header(self, status: int):
        self._status = status
        self._handler.send_response(status)

    def get_status_string(self) -> str:
        return str(self._status)