import logging
from typing import Any

from fastapi import APIRouter, Request

from config.application import app_settings
from src.algorithms.lab1 import load_variant, check_lab
from src.datamodels.user_answers import AnswerLab1


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/lab1", tags=["protected"])


@router.get("/", tags=["html"])
async def get_lab1_page(request: Request):
    templates = app_settings.ui.templates

    variant = load_variant(user_id=None)  # TODO: valid id from database

    web_context = {
        "request": request,
        **variant
    }

    return templates.TemplateResponse("lab1.html", context=web_context)  # TODO: create correct page


@router.post("/check", tags=["checker"])
async def check(request: Request, user_answer: AnswerLab1) -> dict[str, Any]:
    # TODO: release correct functional after auth
    return {
        "verdict": check_lab(user_id=None, user_answers=dict(user_answer))
    }
