import logging

from fastapi import APIRouter, Request

from config.application import app_settings


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_home_page(request: Request):
    templates = app_settings.ui.templates
    web_context = {
        "request": request
    }

    return templates.TemplateResponse("main.html", context=web_context)
