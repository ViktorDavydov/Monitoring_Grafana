"""Prometheus metrics definitions for the demo application."""

from prometheus_client import Counter, Gauge, Histogram, Summary


# HTTP requests total counter
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['pattern', 'method', 'status']
)

# Current inflight requests gauge
http_requests_current = Gauge(
    'http_requests_inflight_current',
    'Current HTTP requests in flight'
)

# Maximum inflight requests gauge
http_requests_inflight_max = Gauge(
    'http_requests_inflight_max',
    'Maximum HTTP requests in flight allowed'
)

# HTTP request duration histogram
http_requests_duration_histogram = Histogram(
    'http_request_duration_seconds_histogram',  # Fixed typo from original
    'HTTP request duration in seconds (histogram)',
    ['pattern', 'method'],
    buckets=[
        0.1,   # 100 ms
        0.2,   # 200 ms
        0.25,  # 250 ms
        0.5,   # 500 ms
        1,     # 1 s
    ]
)

# HTTP request duration summary
http_requests_duration_summary = Summary(
    'http_request_duration_seconds_summary',
    'HTTP request duration in seconds (summary)',
    ['pattern', 'method']
)


def register_metrics():
    """Register all metrics with Prometheus.
    
    This function can be called to ensure all metrics are properly registered.
    In prometheus_client, metrics are automatically registered when created,
    but this function provides an explicit registration point if needed.
    """
    # Metrics are automatically registered when created in prometheus_client
    # This function is kept for compatibility with the Go version
    pass





