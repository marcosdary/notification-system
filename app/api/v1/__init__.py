from fastapi import APIRouter

from app.api.v1.routers import file_router


router = APIRouter()

router.include_router(file_router.router, prefix="/file", tags=["file"])