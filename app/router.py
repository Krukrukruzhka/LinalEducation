from fastapi import APIRouter

from app.routes import (
    root,
    auth,
    api,
    linal_routes
)


main_router = APIRouter()
main_router.include_router(auth.router)
main_router.include_router(root.router)
main_router.include_router(api.router)
main_router.include_router(linal_routes.router)
