import uuid

from src.schemas.certificate import SCertificate, SCertificateAdd
from src.repositories.base import AbstractRepository


class CertificateService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def create(self, item: SCertificateAdd) -> SCertificate:
        item_dict = item.model_dump()
        item_to_db = SCertificate(**item_dict, id=uuid.uuid4())
        item_dict = item_to_db.model_dump()
        item = await self.repository.create(item_dict)
        return item

    async def getAll(self) -> list[SCertificate]:
        return await self.repository.getAll()

    async def update(self, id: uuid.UUID, data: dict) -> bool:
        if data.get("expire_date") == "":
            data["expire_date"] = None
        print(f"{id} - {data}")
        print(data.get("expire_date"))
        return await self.repository.update(id, data)

    async def delete(self, id: uuid.UUID):
        return await self.repository.delete(id)

    async def deleteAll(self):
        return await self.repository.deleteAll()
