from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.main_router import router
from src.database.db import delete_tables, create_tables
from src.repositories.user import UserRepository
from src.services.user import UserService
from src.utils.redis_client import get_redis
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Включение")
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова")
    service = UserService(UserRepository)
    await service.createAdmin()
    print("Администратор установлен")
    redis = await get_redis()
    await redis.ping()
    print("Redis подключен")
    yield
    await redis.close()
    print("Выключение")


app = FastAPI(lifespan=lifespan, docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"],
    allow_credentials=True
)

app.include_router(router)

# === Метрики ===

# Количество HTTP-запросов
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

# Время обработки запроса
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency",
    ["method", "endpoint"],
)


# === Middleware для автоматического сбора ===

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    endpoint = request.url.path
    method = request.method
    status = response.status_code

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    return response


# === Эндпоинт для Prometheus ===

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
