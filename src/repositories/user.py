from src.database.db import User
from src.repositories.base import SQLAlchemyRepository
from src.schemas.user import SUser


class UserRepository(SQLAlchemyRepository):
    model = User
    schema = SUser

    async def getByUsername(self, username: str) -> SUser | None:
        return await self.getOneBy(self.model.username, username)
