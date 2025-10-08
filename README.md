# Monitoring Grafana (Python)

Демо-проект для курса **«Мониторинг в Grafana»**: минимальное Python‑приложение с экспортом Prometheus‑метрик и отдельным генератором нагрузки.

### Что внутри
- **demoapp/cmd/app** — HTTP‑сервер с эндпойнтами и `/metrics`.
- **demoapp/cmd/load** — генератор нагрузки (многопоточный).
- **demoapp/internal** — метрики и middleware.

## Быстрый старт (Docker)

Ниже — два варианта: через `docker build && docker run` или `docker-compose`.

### Вариант A. Чистый Docker

1) Соберите образ приложения:

```bash
docker build -t demoapp:latest -f - . <<'DOCKERFILE'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "-m", "demoapp.cmd.app.main"]
DOCKERFILE
```

2) (Опционально) Соберите образ генератора нагрузки:

```bash
docker build -t demo-load:latest -f - . <<'DOCKERFILE'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
CMD ["python", "-m", "demoapp.cmd.load.main"]
DOCKERFILE
```

3) Создайте сеть и запустите контейнеры:

```bash
docker network create demo-net || true
docker run --rm -d --name app --network demo-net -p 8080:8080 \
  -e HTTP_REQUESTS_INFLIGHT_MAX=20 \
  demoapp:latest

# Генератор нагрузки будет обращаться к сервису по имени контейнера `app`
docker run --rm -d --name load --network demo-net \
  -e HTTP_REQUESTS_SUCCESSFUL_MAX=15 \
  -e HTTP_REQUESTS_ERROR_MAX=5 \
  -e TARGET_BASE_URL=http://app:8080 \
  demo-load:latest
```

4) Проверьте метрики:

```bash
curl http://localhost:8080/metrics
```

Остановка:

```bash
docker rm -f load app
docker network rm demo-net
```

### Вариант B. docker-compose

Создайте файл `docker-compose.yml` рядом с `README.md`:

```yaml
version: "3.9"
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.app
    environment:
      HTTP_REQUESTS_INFLIGHT_MAX: 20
    ports:
      - "8080:8080"

  load:
    build:
      context: .
      dockerfile: Dockerfile.load
    environment:
      HTTP_REQUESTS_SUCCESSFUL_MAX: 15
      HTTP_REQUESTS_ERROR_MAX: 5
      TARGET_BASE_URL: http://app:8080
    depends_on:
      - app
```

И два простых Dockerfile:

```dockerfile
# Dockerfile.app
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "-m", "demoapp.cmd.app.main"]
```

```dockerfile
# Dockerfile.load
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "demoapp.cmd.load.main"]
```

Запуск:

```bash
docker compose up --build -d
# Проверка
curl http://localhost:8080/metrics
```

Остановка:

```bash
docker compose down -v
```

## Эндпойнты приложения
- `GET /code-2xx` — случайный 2xx.
- `GET /code-4xx` — случайный 4xx.
- `GET /code-5xx` — случайный 5xx.
- `GET /ms-200` — ответ с задержкой до 200ms и `200`.
- `GET /ms-500` — задержка до 500ms и `200`.
- `GET /ms-1000` — задержка до 1000ms и `200`.
- `GET /metrics` — метрики Prometheus.

## Метрики Prometheus
Экспортируются через `prometheus_client` и обновляются middleware:

| Метрика                               | Тип       | Лейблы                         | Описание |
|---------------------------------------|-----------|--------------------------------|----------|
| `http_requests_total`                 | counter   | `pattern`, `method`, `status`  | Кол-во обработанных HTTP‑запросов |
| `http_requests_inflight_current`      | gauge     | —                              | Текущие обрабатываемые запросы |
| `http_requests_inflight_max`          | gauge     | —                              | Максимум одновременных запросов (настраивается) |
| `http_request_duration_seconds_histogram` | histogram | `pattern`, `method`            | Гистограмма времени обработки |
| `http_request_duration_seconds_summary`   | summary   | `pattern`, `method`            | Сводка времени обработки |

## Переменные окружения
Можно передавать как обычные env‑переменные перед запуском процесса.

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `HTTP_REQUESTS_INFLIGHT_MAX` | Верхняя граница `http_requests_inflight_max` в приложении | `20` |
| `HTTP_REQUESTS_SUCCESSFUL_MAX` | Верхняя граница успешных запросов в генераторе нагрузки | `15` |
| `HTTP_REQUESTS_ERROR_MAX` | Верхняя граница ошибочных запросов в генераторе нагрузки | `5` |

Пример запуска с кастомными значениями:

```bash
HTTP_REQUESTS_INFLIGHT_MAX=50 \
HTTP_REQUESTS_SUCCESSFUL_MAX=25 \
HTTP_REQUESTS_ERROR_MAX=10 \
python -m demoapp.cmd.app.main
```

## Интеграция с Prometheus и Grafana
Если Prometheus и Grafana тоже запущены в Compose, используйте имя сервиса `app` как `target`:

```yaml
scrape_configs:
  - job_name: 'demoapp'
    static_configs:
      - targets: ['app:8080']
```

Если Prometheus вне Docker, таргет будет `localhost:8080` (или хост/порт соответствующего сервера).

В Grafana добавьте Prometheus‑датасорс и постройте панели по счетчикам и задержкам.

## Структура репозитория
```
demoapp/
├─ cmd/
│  ├─ app/   # сервер
│  └─ load/  # генератор нагрузки
└─ internal/
   ├─ helpers/
   ├─ metrics/
   └─ middleware/
docs/
requirements.txt
README.md
```

## Требования
- Docker / Docker Desktop
- (Опционально) docker-compose / Docker Compose v2
- Для локального запуска без контейнеров: Python 3.10+ и `pip`

Полезные ссылки:
- Документация Prometheus: https://prometheus.io/docs/
- Документация Grafana: https://grafana.com/docs/