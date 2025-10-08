from prometheus_client import Counter, Gauge, Histogram, Summary
# from prometheus_client.metrics import Objectives

HttpRequestsTotal = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['pattern', 'method', 'status']
)

HttpRequestsCurrent = Gauge(
    'http_requests_inflight_current',
    'Current inflight HTTP requests',
    []
)

HttpRequestsInflightMax = Gauge(
    'http_requests_inflight_max', 
    'Max inflight HTTP requests',
    []
)

HttpRequestsDurationHistogram = Histogram(
    'http_request_duration_seconds_histogram',
    'HTTP request duration histogram',
    ['pattern', 'method'],
    buckets=[0.1, 0.2, 0.25, 0.5, 1.0]
)

HttpRequestsDurationSummary = Summary(
    'http_request_duration_seconds_summary', 
    'HTTP request duration summary',
    ['pattern', 'method'],
    # objectives=Objectives({
    #     0.99: 0.001,
    #     0.95: 0.01,
    #     0.5: 0.05
    # }),
    
)