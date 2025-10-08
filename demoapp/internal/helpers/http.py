import random
import time
from http import HTTPStatus
from typing import List

def random_duration_ms(max_ms: int) -> float:
    min_ms = 1
    r = random.randint(min_ms, max_ms)
    return r / 1000.0

def random_2xx() -> int:
    statuses = [
        HTTPStatus.OK,                    # 200
        HTTPStatus.CREATED,               # 201
        HTTPStatus.ACCEPTED,              # 202
        HTTPStatus.NON_AUTHORITATIVE_INFORMATION,  # 203
        HTTPStatus.NO_CONTENT,            # 204
    ]
    return random.choice(statuses)

def random_4xx() -> int:
    statuses = [
        HTTPStatus.BAD_REQUEST,           # 400
        HTTPStatus.UNAUTHORIZED,          # 401
        HTTPStatus.FORBIDDEN,             # 403
        HTTPStatus.NOT_FOUND,             # 404
        HTTPStatus.TOO_MANY_REQUESTS,     # 429
    ]
    return random.choice(statuses)

def random_5xx() -> int:
    statuses = [
        HTTPStatus.INTERNAL_SERVER_ERROR, # 500
        HTTPStatus.NOT_IMPLEMENTED,       # 501
        HTTPStatus.BAD_GATEWAY,           # 502
        HTTPStatus.SERVICE_UNAVAILABLE,   # 503
        HTTPStatus.GATEWAY_TIMEOUT,       # 504
    ]
    return random.choice(statuses)
