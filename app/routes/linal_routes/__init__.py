from fastapi import APIRouter

from app.routes.linal_routes import (
    lab1
)


router = APIRouter(prefix='/linal', tags=["linal"])
router.include_router(lab1.router)
