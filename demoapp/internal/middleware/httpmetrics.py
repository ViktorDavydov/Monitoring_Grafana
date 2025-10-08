import time
from urllib.parse import urlparse
from demoapp.internal.metrics import metrics
from demoapp.internal.helpers.responsewriter import StatusResponseWriter

def http_metrics_middleware(handler):
    """
    Middleware для сбора метрик HTTP запросов
    """
    def wrapper(self):
        start_time = time.time()
        
        # Создаем StatusResponseWriter для отслеживания статуса
        status_writer = StatusResponseWriter(self)
        
        # Получаем информацию о запросе
        pattern = self.get_route_pattern()
        method = self.command  # GET, POST, etc
        
        # Вызываем оригинальный обработчик
        try:
            handler(self)
        except Exception as e:
            # Если произошла ошибка, устанавливаем статус 500
            status_writer.write_header(500)
            raise e
        
        # Вычисляем время выполнения
        elapsed_seconds = time.time() - start_time
        status = status_writer.get_status_string()
        
        # Обновляем метрики
        metrics.HttpRequestsTotal.labels(
            pattern=pattern,
            method=method,
            status=status
        ).inc()
        
        metrics.HttpRequestsDurationHistogram.labels(
            pattern=pattern,
            method=method
        ).observe(elapsed_seconds)
        
        metrics.HttpRequestsDurationSummary.labels(
            pattern=pattern,
            method=method
        ).observe(elapsed_seconds)
    
    return wrapper

def inflight_requests_middleware(handler):
    """
    Middleware для отслеживания количества текущих выполняющихся запросов
    """
    def wrapper(self):
        # Увеличиваем счетчик текущих запросов
        metrics.HttpRequestsCurrent.inc()
        
        try:
            # Вызываем оригинальный обработчик
            handler(self)
        finally:
            # Уменьшаем счетчик текущих запросов (гарантированно выполнится)
            metrics.HttpRequestsCurrent.dec()
    
    return wrapper

def get_route_pattern(self):
    """
    Определяет паттерн маршрута на основе пути
    """
    path = urlparse(self.path).path
    
    # Сопоставляем путь с известными паттернами
    route_patterns = {
        '/code-2xx': '/code-2xx',
        '/code-4xx': '/code-4xx', 
        '/code-5xx': '/code-5xx',
        '/ms-200': '/ms-200',
        '/ms-500': '/ms-500',
        '/ms-1000': '/ms-1000',
        '/metrics': '/metrics'
    }
    
    return route_patterns.get(path, path)  # возвращаем паттерн или оригинальный путь