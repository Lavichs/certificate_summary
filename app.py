from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.main_router import router
from src.database.db import delete_tables, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Включение")
    # await delete_tables()
    # print("База очищена")
    # await create_tables()
    # print("База готова")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan, docs_url="/api/docs")


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(router)