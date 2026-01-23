from fastapi import APIRouter
from src.api.routes.certificates import router as certificate_router

router = APIRouter(prefix="/api")

router.include_router(certificate_router)
