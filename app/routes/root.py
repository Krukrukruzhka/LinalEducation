import logging

from fastapi import APIRouter, Request, Depends

from config.application import app_settings
from src.utils.auth_utils import get_username_by_jwt, get_token_from_cookie
from src.datamodels.user import RolesEnum


logger = logging.getLogger(__name__)
router = APIRouter(tags=["html"])


@router.get("/", tags=["protected"])
async def get_home_page(request: Request, token: str = Depends(get_token_from_cookie)):
    username = get_username_by_jwt(token)

    user_data = await app_settings.database.get_basic_data_by_username(username)

    templates = app_settings.ui.templates
    web_context = {
        "request": request,
        "user_data": user_data
    }

    return templates.TemplateResponse("basic.html", context=web_context)


@router.get("/profile", tags=["protected"])
async def get_profile_page(request: Request, token: str = Depends(get_token_from_cookie)):
    username = get_username_by_jwt(token)

    user_data = await app_settings.database.get_basic_data_by_username(username)
    user = user_data.user

    templates = app_settings.ui.templates
    web_context = {
        "request": request,
        "user_data": user_data
    }

    if user.role_id == RolesEnum.TEACHER.id:
        web_context.update({"all_groups_and_students": await app_settings.database.get_all_groups_and_students()})
        return templates.TemplateResponse("teacher.html", context=web_context)
    else:
        return templates.TemplateResponse("student.html", context=web_context)
