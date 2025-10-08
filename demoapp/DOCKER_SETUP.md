# Docker & DevContainer Setup - Pure Python Edition

## Особенности

Приложение переписано на **чистом Python** без фреймворков:
- ✅ Использует только стандартную библиотеку Python
- ✅ Единственная внешняя зависимость: `prometheus-client`
- ✅ HTTP сервер на базе `http.server.HTTPServer`
- ✅ HTTP клиент на базе `urllib`
- ✅ Многопоточность через `threading`

## Запуск в DevContainer

1. Откройте проект в VSCode
2. При появлении уведомления о DevContainer нажмите "Reopen in Container"
3. Или используйте команду: `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

DevContainer автоматически:
- Установит Python 3.11
- Установит только prometheus-client
- Настроит расширения VSCode для Python

## Доступные конфигурации запуска в VSCode

В меню Run and Debug доступны:

1. **Python: App Server** - запуск основного приложения
2. **Python: Load Generator** - запуск генератора нагрузки

## Переменные окружения

```bash
# Максимальное количество одновременных запросов
HTTP_REQUESTS_INFLIGHT_MAX=20.0

# Максимальное количество успешных запросов в батче
HTTP_REQUESTS_SUCCESSFUL_MAX=15

# Максимальное количество ошибочных запросов в батче
HTTP_REQUESTS_ERROR_MAX=5
```

## Эндпоинты

- `GET /code-2xx` - Случайный 2xx статус код
- `GET /code-4xx` - Случайный 4xx статус код  
- `GET /code-5xx` - Случайный 5xx статус код
- `GET /ms-200` - Задержка до 200мс
- `GET /ms-500` - Задержка до 500мс
- `GET /ms-1000` - Задержка до 1000мс
- `GET /metrics` - Метрики Prometheus

## Быстрый старт

### В DevContainer:
1. `F5` → "Python: App Server"
2. `F5` → "Python: Load Generator"

### Локально:
```bash
cd demoapp
pip install prometheus-client
python run_server.py    # В одном терминале
python run_load.py      # В другом терминале
```

### Docker:
```bash
cd demoapp
docker build -t demoapp .
docker run -p 8080:8080 demoapp
```

## Архитектура

```
┌─────────────────┐    ┌─────────────────┐
│  Load Generator │───▶│   HTTP Server   │
│   (urllib)      │    │ (http.server)   │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ Prometheus  │
                       │  Metrics    │
                       └─────────────┘
```

Максимально простая архитектура без фреймворков!



