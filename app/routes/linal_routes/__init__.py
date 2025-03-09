from fastapi import APIRouter

from app.routes.linal_routes import (
    lab1,
    lab7,
    lab8
)


router = APIRouter(prefix='/linal', tags=["linal"])
router.include_router(lab1.router)
router.include_router(lab7.router)
router.include_router(lab8.router)
