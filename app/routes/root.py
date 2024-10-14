import logging

from fastapi import APIRouter, Request

from src.state.application import app_state


logger = logging.getLogger(__name__)
router = APIRouter()
templates = app_state.ui.templates


@router.get("/")
async def get_home_page(request: Request):
    web_context = {
        "request": request
    }

    return templates.TemplateResponse("main.html", context=web_context)
