from fastapi import APIRouter

from app.routes import (
    root,
    lab1
)


unprotected_routers = APIRouter()
unprotected_routers.include_router(root.router)
unprotected_routers.include_router(lab1.router)
