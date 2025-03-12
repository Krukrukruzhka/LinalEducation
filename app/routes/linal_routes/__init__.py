from fastapi import APIRouter

from app.routes.linal_routes import (
    lab1,
    lab4,
    lab5
)


router = APIRouter(prefix='/linal', tags=["linal"])
router.include_router(lab1.router)
router.include_router(lab4.router)
router.include_router(lab5.router)
