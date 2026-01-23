from src.database.db import Certificate
from src.repositories.base import SQLAlchemyRepository
from src.schemas.certificate import SCertificate


class CertificateRepository(SQLAlchemyRepository):
    model = Certificate
    schema = SCertificate
