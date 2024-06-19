from fastapi import APIRouter
from app.api.routes.health import health_router
from app.api.routes import auth
from app.api.routes import file

#==========================================================#
router = APIRouter()
#===========================================================#

router.include_router(health_router , prefix="/health")

#==============================================================#

router.include_router(auth.auth_router)

#==============================================================#

router.include_router(file.file_router)

#==============================================================#