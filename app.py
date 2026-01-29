from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.main_router import router
from src.database.db import delete_tables, create_tables
from src.repositories.user import UserRepository
from src.services.user import UserService
from src.utils.redis_client import get_redis


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
