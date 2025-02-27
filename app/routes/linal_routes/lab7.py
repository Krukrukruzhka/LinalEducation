import datetime
import logging
from typing import Any

from fastapi import APIRouter, Request
from fastapi import Depends

from config.application import app_settings
from src.algorithms import linear_algebra
from src.datamodels.labs import LinalLab7Response
from src.utils.auth_utils import get_username_by_jwt, get_token_from_cookie


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/lab7", tags=["protected"])


@router.get("/", tags=["html"])
async def get_lab7_page(request: Request, token: str = Depends(get_token_from_cookie)):
    templates = app_settings.ui.templates

    username = get_username_by_jwt(token)
    user_data = await app_settings.database.get_basic_data_by_username(username)

    current_student = user_data.student
    current_user = user_data.user

    if current_student is None:
        raise Exception("Maybe you not a student")  # TODO: change to correct HTTPException

    variant = await app_settings.database.load_linal_lab7_variant(student_id=current_student.id)

    web_context = {
        "request": request,
        "variant": variant.dict(),
        "user": current_user,
        "is_solved": current_student.marks[6].result,
        "user_data": user_data
    }

    return templates.TemplateResponse("linear_algebra/lab7.html", context=web_context)


@router.post("/check", tags=["checker"])
async def check_lab7(request: Request, user_answer: LinalLab7Response, token: str = Depends(get_token_from_cookie)) -> dict[str, Any]:
    username = get_username_by_jwt(token)
    current_student = await app_settings.database.get_student_by_username(username)
    if current_student is None:
        raise Exception("Maybe you not a student")  # TODO: change to correct HTTPException

    variant = await app_settings.database.load_linal_lab7_variant(student_id=current_student.id)

    is_correct_answer = linear_algebra.lab7.check_lab(condition=variant, user_answer=user_answer)

    marks = current_student.marks
    if is_correct_answer and not marks[6].result:  # TODO: if two requests from different labs arrive at the same time, the score may get lost
        marks[6].result = True
        marks[6].approve_date = str(datetime.datetime.now().date())
        await app_settings.database.update_user_marks(username=username, new_marks=marks)

    return {
        "verdict": is_correct_answer
    }
