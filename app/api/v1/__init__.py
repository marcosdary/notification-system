from fastapi import APIRouter

from app.api.v1.routers import file_route


router = APIRouter()

router.include_router(file_route.router, prefix="/file", tags=["file"])