import logging

from fastapi import APIRouter, Request, Depends

from config.application import app_settings
from src.utils.auth_utils import get_username_by_jwt, get_token_from_cookie


logger = logging.getLogger(__name__)
router = APIRouter(tags=["html"])


@router.get("/", tags=["protected"])
async def get_home_page(request: Request, token: str = Depends(get_token_from_cookie)):
    username = get_username_by_jwt(token)
    user = await app_settings.database.get_user_by_username(username)

    templates = app_settings.ui.templates
    web_context = {
        "request": request,
        "user": user.dict()
    }

    return templates.TemplateResponse("basic.html", context=web_context)


@router.get("/profile", tags=["protected"])
async def get_profile_page(request: Request, token: str = Depends(get_token_from_cookie)):
    username = get_username_by_jwt(token)
    user = await app_settings.database.get_user_by_username(username)

    templates = app_settings.ui.templates
    web_context = {
        "request": request,
        "user": user.dict()
    }

    # TODO: here should also be a developer's page.
    if user.role_id == 1:  # TODO: change to enum
        teacher = await app_settings.database.get_teacher_by_username(username)
        web_context.update({"teacher": teacher.dict()})
        return templates.TemplateResponse("teacher.html", context=web_context)
    else:
        student = await app_settings.database.get_student_by_username(username)
        web_context.update({"student": student.dict()})
        return templates.TemplateResponse("student.html", context=web_context)
