from demoapp.internal.metrics import metrics

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