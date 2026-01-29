from fastapi import APIRouter
from src.api.routes.certificates import router as certificate_router
from src.api.routes.users import router as user_router

router = APIRouter(prefix="/api")

router.include_router(certificate_router)
router.include_router(user_router)
