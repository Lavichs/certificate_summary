# from src.repositories.user import UserRepository
# from src.services.user import UserService
from src.repositories.certificate import CertificateRepository
from src.services.certificate import CertificateService


def certificate_service() -> CertificateService:
    return CertificateService(CertificateRepository)


# def user_service() -> UserService:
#     return UserService(UserRepository)
