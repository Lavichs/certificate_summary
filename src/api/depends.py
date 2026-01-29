import json

from fastapi import Cookie, Depends, HTTPException, status
from redis.asyncio import Redis

from config import settings
from src.repositories.user import UserRepository
from src.services.user import UserService
from src.repositories.certificate import CertificateRepository
from src.services.certificate import CertificateService
from src.utils.redis_client import get_redis


def certificate_service() -> CertificateService:
    return CertificateService(CertificateRepository)


def user_service() -> UserService:
    return UserService(UserRepository)


async def get_session_data(
    session_id: str = Cookie(alias=settings.COOKIE_SESSION_ID_KEY),
    redis: Redis = Depends(get_redis),
) -> dict:
    session = await redis.get(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    session = json.loads(session)
    return session
