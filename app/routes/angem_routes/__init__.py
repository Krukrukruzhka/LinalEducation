from fastapi import APIRouter

from app.routes.angem_routes import (
    lab8
)


router = APIRouter(prefix='/angem', tags=["angem"])
router.include_router(lab8.router)
