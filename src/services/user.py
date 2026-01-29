import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException

from config import settings
from src.repositories.base import AbstractRepository
from src.schemas.user import SCredentials, SUser
from src.utils.ldap_auth import LDAP_AUTH


class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def getUserByUsername(self, username: str):
        return await self.repository.getByUsername(username)

    async def create(self, credentials: SCredentials, is_operator: bool):
        return await self.repository.create(
            {
                "id": uuid.uuid4(),
                "username": credentials.username,
                "isOperator": is_operator,
            }
        )

    async def createAdmin(self):
        if await self.getUserByUsername("sysadm") is None:
            return await self.create(
                SCredentials(username="sysadm", password=""), is_operator=True
            )

    async def login(self, credentials: SCredentials):
        if credentials.username == "sysadm" and credentials.password == settings.ADMIN_PASSWORD:
            return {
                "username": "sysadm",
                "isOperator": True,
            }

        if not LDAP_AUTH(settings.DOMAIN, credentials.username, credentials.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user: SUser = await self.repository.getByUsername(credentials.username)
        if user is None:
            user = await self.create(credentials, False)

        return {
            "username": user.username,
            "isOperator": user.isOperator,
        }

    # async def login(self, credentials: SCredentials):
    #     if not LDAP_AUTH(settings.DOMAIN, credentials.username, credentials.password):
    #         raise HTTPException(status_code=401, detail="Invalid credentials")
    #
    #     user: SUser = await self.repository.getByUsername(credentials.username)
    #     if user is None:
    #         user = await self.create(credentials)
    #
    #     expire = datetime.now() + timedelta(minutes=settings.JWT_MINUTES_LIFETIME)
    #     token = security.create_access_token(uid=str(user.id), expiry=expire)
    #     return {
    #         "access_token": token,
    #         "access": json.loads(user.access),
    #         "username": user.username,
    #     }
    #
    # async def update(self, id, username: str, access: dict):
    #     return await self.repository.update(id, {
    #         "username": username,
    #         "access": json.dumps(access)
    #     })
    #
    # async def getUserAccess(self, id):
    #     return (await self.repository.getById(id)).access
    #
    # async def getUserByUsername(self, username):
    #     return await self.repository.getByUsername(username)
