import json
import uuid
from time import time
from typing import Annotated
from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from redis.asyncio import Redis
from fastapi.encoders import jsonable_encoder

from config import settings
from src.api.depends import user_service, get_session_data
from src.schemas.user import SCredentials
from src.services.user import UserService
from src.utils.redis_client import get_redis

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

security = HTTPBasic()


@router.post("/login")
async def login(
    response: Response,
    credentials: SCredentials,
    user_service: Annotated[UserService, Depends(user_service)],
    redis: Redis = Depends(get_redis),
):
    user_data = await user_service.login(credentials)
    session_id = uuid.uuid4().hex
    user_cookie = {
        "username": credentials.username,
        "isOperator": user_data.get("isOperator"),
        "login_at": int(time()),
    }
    await redis.set(session_id, json.dumps(jsonable_encoder(user_cookie)), ex=settings.CACHE_LIFETIME)
    response.set_cookie(settings.COOKIE_SESSION_ID_KEY, session_id)
    response.set_cookie("my-cookie", "session_id")
    response.set_cookie("any-cookie", "any-value")
    return {"result": "ok"}


@router.get("/check-cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}!",
        **user_session_data,
    }

