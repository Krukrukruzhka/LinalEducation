from fastapi import APIRouter

from app.routes import root


unprotected_routers = APIRouter()
unprotected_routers.include_router(root.router)
