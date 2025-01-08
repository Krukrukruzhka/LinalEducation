import logging

from fastapi import APIRouter, Request, Depends

from config.application import app_settings
from src.utils.auth_utils import get_username_by_jwt, get_token_from_cookie


logger = logging.getLogger(__name__)
router = APIRouter(tags=["html"])


@router.get("/", tags=["unprotected"])
async def get_home_page(request: Request):
    templates = app_settings.ui.templates
    web_context = {
        "request": request
    }

    return templates.TemplateResponse("main.html", context=web_context)


@router.get("/profile", tags=["protected"])
async def get_profile_page(request: Request, token: str = Depends()):
    templates = app_settings.ui.templates
    web_context = {
        "request": request
    }

    return templates.TemplateResponse("main.html", context=web_context)