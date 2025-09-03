"""Response writer wrapper for capturing HTTP status codes."""

from http import HTTPStatus


class StatusResponseWriter:
    """Wrapper for capturing HTTP response status codes."""
    
    def __init__(self, response_writer=None):
        """Initialize the status response writer.
        
        Args:
            response_writer: Optional response writer to wrap
        """
        self.response_writer = response_writer
        self.status = HTTPStatus.OK.value  # Default to 200
    
    def write_header(self, status):
        """Set the HTTP status code.
        
        Args:
            status (int): HTTP status code
        """
        self.status = status
        if self.response_writer:
            self.response_writer.write_header(status)
    
    def get_status_string(self):
        """Get the status code as a string.
        
        Returns:
            str: Status code as string
        """
        return str(self.status)
    
    def get_status(self):
        """Get the status code as an integer.
        
        Returns:
            int: HTTP status code
        """
        return self.status





