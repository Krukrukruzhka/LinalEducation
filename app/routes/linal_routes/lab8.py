import logging
from typing import Any

from fastapi import APIRouter, Request
from fastapi import Depends

from config.application import app_settings
from src.algorithms import linear_algebra
from src.datamodels.labs import LinalLab8Response
from src.utils.auth_utils import get_token_from_cookie

from src.utils import rout_utils


LAB_NUMBER = 8
CurrentLabResponse = LinalLab8Response

logger = logging.getLogger(__name__)
router = APIRouter(prefix=f"/lab{LAB_NUMBER}", tags=["protected"])


@router.get("/", tags=["html"])
async def get_lab_page(request: Request, token: str = Depends(get_token_from_cookie)):
    return await rout_utils.get_lab_page_utils(
        request=request,
        token=token,
        lab_number=LAB_NUMBER,
        course_name="linear_algebra",
        load_variant_func=app_settings.database.load_linal_lab8_variant
    )


@router.post("/check", tags=["checker"])
async def check_lab(request: Request, user_answer: CurrentLabResponse, token: str = Depends(get_token_from_cookie)) -> dict[str, Any]:
    return await rout_utils.check_lab_utils(
        user_answer=user_answer,
        token=token,
        lab_number=LAB_NUMBER,
        load_variant_func=app_settings.database.load_linal_lab8_variant,
        check_lab_func=linear_algebra.lab8.check_lab
    )
