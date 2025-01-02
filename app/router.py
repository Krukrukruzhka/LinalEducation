from fastapi import APIRouter

from app.routes import (
    root,
    auth,
    lab1
)


main_router = APIRouter()
main_router.include_router(auth.router)
main_router.include_router(root.router)
main_router.include_router(lab1.router)
