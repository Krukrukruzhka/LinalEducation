from fastapi import APIRouter

from app.routes.linal_routes import (
    lab1,
    lab2,
    lab3,
    lab4,
    lab5,
    lab6,
    lab7,
    lab8,
    lab9,
    lab10,
    lab11,
    lab12,
    lab13,
    lab14,
    lab15
)


router = APIRouter(prefix='/linal', tags=["linal"])
router.include_router(lab1.router)
router.include_router(lab2.router)
router.include_router(lab3.router)
router.include_router(lab4.router)
router.include_router(lab5.router)
router.include_router(lab6.router)
router.include_router(lab7.router)
router.include_router(lab8.router)
router.include_router(lab9.router)
router.include_router(lab10.router)
router.include_router(lab11.router)
router.include_router(lab12.router)
router.include_router(lab13.router)
router.include_router(lab14.router)
router.include_router(lab15.router)