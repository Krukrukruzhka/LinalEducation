import logging
from typing import Any

from fastapi import APIRouter, Request
from fastapi import Depends

from config.application import app_settings
from src.algorithms import lab1
from src.datamodels.labs import Lab1Response
from src.utils.auth_utils import get_username_by_jwt, get_token_from_cookie


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/lab1", tags=["protected"])


@router.get("/", tags=["html"])
async def get_lab1_page(request: Request, token: str = Depends(get_token_from_cookie)):
    templates = app_settings.ui.templates

    username = get_username_by_jwt(token)
    current_student = await app_settings.database.get_student_by_username(username)
    if current_student is None:
        raise Exception("Maybe you not a student")  # TODO: change to correct HTTPException

    variant = await app_settings.database.load_lab1_variant(student_id=current_student.id)

    web_context = {
        "request": request,
        **variant.dict(),
        "is_solved": current_student.marks[0]
    }

    return templates.TemplateResponse("lab1.html", context=web_context)


@router.post("/check", tags=["checker"])
async def check_lab1(request: Request, user_answer: Lab1Response, token: str = Depends(get_token_from_cookie)) -> dict[str, Any]:
    username = get_username_by_jwt(token)
    current_student = await app_settings.database.get_student_by_username(username)
    if current_student is None:
        raise Exception("Maybe you not a student")  # TODO: change to correct HTTPException

    variant = await app_settings.database.load_lab1_variant(student_id=current_student.id)

    is_correct_answer = lab1.check_lab(condition=variant, user_answer=user_answer)

    if is_correct_answer:  # TODO: if two requests arrive at the same time, the score may get lost
        marks = current_student.marks
        marks[0] = True
        await app_settings.database.update_marks_by_username(username=username, new_marks=marks)

    return {
        "verdict": is_correct_answer
    }
