import datetime
import logging
from typing import Any
from collections.abc import Callable

from fastapi import Request
from pydantic import BaseModel

from config.application import app_settings
from src.utils.auth_utils import get_username_by_jwt


logger = logging.getLogger(__name__)


async def get_lab_page_utils(
        request: Request,
        token: str,
        lab_number: int,
        course_name: str,
        load_variant_func: Callable[[int], Any]
):
    templates = app_settings.ui.templates

    username = get_username_by_jwt(token)
    user_data = await app_settings.database.get_basic_data_by_username(username)

    current_student = user_data.student
    current_user = user_data.user

    if course_name == "linal":
        is_solved = current_student.linal_marks[lab_number - 1].result
    elif course_name == "angem":
        is_solved = current_student.angem_marks[lab_number - 1].result
    else:
        raise Exception("Unknown course")

    if current_student is None:
        raise Exception("Maybe you not a student")  # TODO: change to correct HTTPException

    variant = await load_variant_func(student_id=current_student.id)
    web_context = {
        "request": request,
        "variant": variant.dict(),
        "user": current_user,
        "is_solved": is_solved,
        "user_data": user_data
    }

    return templates.TemplateResponse(f"{course_name}/lab{lab_number}.html", context=web_context)


async def check_lab_utils(
        user_answer: BaseModel,
        token: str,
        lab_number: int,
        load_variant_func: Callable[[int], Any],
        check_lab_func: Callable[[BaseModel, BaseModel], Any],
        course_name: str
) -> dict[str, Any]:

    username = get_username_by_jwt(token)
    current_student = await app_settings.database.get_student_by_username(username)
    if current_student is None:
        raise Exception("Maybe you not a student")  # TODO: change to correct HTTPException

    variant = await load_variant_func(student_id=current_student.id)

    is_correct_answer = check_lab_func(condition=variant, user_answer=user_answer)

    if course_name == "linal":
        marks = current_student.linal_marks
        if is_correct_answer and not marks[lab_number - 1].result:  # TODO: if two requests from different labs arrive at the same time, the score may get lost
            marks[lab_number - 1].result = True
            marks[lab_number - 1].approve_date = str(datetime.datetime.now().date())
            await app_settings.database.update_user_linal_marks(username=username, new_marks=marks)
    elif course_name == "angem":
        marks = current_student.angem_marks
        if is_correct_answer and not marks[
            lab_number - 1].result:  # TODO: if two requests from different labs arrive at the same time, the score may get lost
            marks[lab_number - 1].result = True
            marks[lab_number - 1].approve_date = str(datetime.datetime.now().date())
            await app_settings.database.update_user_angem_marks(username=username, new_marks=marks)
    else:
        raise Exception("Unknown course")

    return {"verdict": is_correct_answer}
