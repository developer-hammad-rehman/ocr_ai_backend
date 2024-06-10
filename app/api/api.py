from fastapi import APIRouter
from app.api.routes.health import health_router
from app.api.routes import auth

router = APIRouter()

router.include_router(health_router , prefix="/health")
router.include_router(auth.auth_router)