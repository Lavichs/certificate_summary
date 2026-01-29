import uuid
from pydantic import BaseModel


class SCredentials(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class SUser(BaseModel):
    id: uuid.UUID
    username: str
    isOperator: bool

    class Config:
        from_attributes = True
