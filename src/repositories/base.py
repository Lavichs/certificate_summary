from typing import List
import uuid
from abc import ABC, abstractmethod
from sqlalchemy import select, insert, update

from src.database.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> any:
        raise NotImplementedError

    @abstractmethod
    async def getAll(self) -> List[any]:
        raise NotImplementedError

    @abstractmethod
    async def getById(self, id: uuid.UUID) -> any:
        raise NotImplementedError

    @abstractmethod
    async def getOneBy(self, field: any, value: any) -> List[any]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: uuid.UUID, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    schema = None

    async def create(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def getAll(self):
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .where(self.model.is_delete == False)
                .order_by(self.model.created_at.desc())
            )
            res = await session.execute(stmt)
            res = [self.schema.model_validate(row[0]) for row in res.all()]
            return res

    async def getDeleted(self):
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .where(self.model.is_delete == True)
                .order_by(self.model.created_at.desc())
            )
            res = await session.execute(stmt)
            res = [self.schema.model_validate(row[0]) for row in res.all()]
            return res

    async def getById(self, id: uuid.UUID):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self.schema.model_validate(model)

    async def getOneBy(self, field: any, value: any):
        async with async_session_maker() as session:
            stmt = select(self.model).where(field == value).limit(1)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self.schema.model_validate(model)

    async def update(self, id: uuid.UUID, data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    async def delete(self, id: uuid.UUID):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values({self.model.is_delete: True})
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
