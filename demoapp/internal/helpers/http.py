"""HTTP helper functions for generating random responses and delays."""

import random
import time
from http import HTTPStatus


def RandomDurationMS(max_ms):
    """Generate random duration in seconds up to max_ms milliseconds.
    
    Args:
        max_ms (int): Maximum milliseconds for the random duration
        
    Returns:
        float: Random duration in seconds
    """
    min_ms = 1
    random_ms = random.randint(min_ms, max_ms)
    return random_ms / 1000.0  # Convert to seconds


def Random2xx():
    """Return a random 2xx HTTP status code.
    
    Returns:
        int: Random 2xx status code
    """
    statuses = [
        HTTPStatus.OK,           # 200
        HTTPStatus.ACCEPTED,     # 202
    ]
    
    # Fix the original Go bug: use len(statuses) instead of len(statuses) - 1
    index = random.randint(0, len(statuses) - 1)
    return int(statuses[index])


def Random4xx():
    """Return a random 4xx HTTP status code.
    
    Returns:
        int: Random 4xx status code
    """
    statuses = [
        HTTPStatus.BAD_REQUEST,          # 400
        HTTPStatus.UNAUTHORIZED,         # 401
        HTTPStatus.NOT_FOUND,           # 404
        HTTPStatus.TOO_MANY_REQUESTS,   # 429
    ]
    
    # Fix the original Go bug: use len(statuses) instead of len(statuses) - 1
    index = random.randint(0, len(statuses) - 1)
    return int(statuses[index])


def Random5xx():
    """Return a random 5xx HTTP status code.
    
    Returns:
        int: Random 5xx status code
    """
    statuses = [
        HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
        HTTPStatus.NOT_IMPLEMENTED,        # 501
        HTTPStatus.SERVICE_UNAVAILABLE,    # 503
        HTTPStatus.GATEWAY_TIMEOUT,        # 504
    ]
    
    # Fix the original Go bug: use len(statuses) instead of len(statuses) - 1
    index = random.randint(0, len(statuses) - 1)
    return int(statuses[index])





