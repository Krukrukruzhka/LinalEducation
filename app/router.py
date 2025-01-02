from fastapi import APIRouter

from app.routes import (
    root,
    auth,
    lab1
)


unprotected_routers = APIRouter()
unprotected_routers.include_router(root.router)
unprotected_routers.include_router(auth.router)
unprotected_routers.include_router(lab1.router)
