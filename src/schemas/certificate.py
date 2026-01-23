import datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field


class SCertificateAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cert_center: str | None  # = Field(default="—")
    fio: str | None
    post: str | None
    organization: str | None
    expire_date: datetime.datetime | None
    status: str | None
    comment: str | None
    is_delete: bool = Field(default=False)


# class SCertificateChange(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     cert_center: str | None = None
#     fio: str | None = None
#     post: str | None = None
#     organization: str | None = None
#     expire_date: datetime.datetime | None = None
#     status: str | None = None
#     comment: str | None = None


class SCertificate(SCertificateAdd):
    id: uuid.UUID
