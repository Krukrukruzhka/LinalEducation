import logging
from fastapi import HTTPException

from fastapi import APIRouter, Request, Depends

from config.application import app_settings
from src.utils.auth_utils import get_username_by_jwt, get_token_from_cookie
from src.datamodels.utils import AdditionalUserInfo, TextWithGroups
from src.datamodels.user import StudentGroup


logger = logging.getLogger(__name__)
router = APIRouter(tags=["api"])


@router.post("/update-additional-info", tags=["protected"])
async def update_additional_info(request: Request, additional_info: AdditionalUserInfo, token: str = Depends(get_token_from_cookie)):
    username = get_username_by_jwt(token)

    user = await app_settings.database.get_user_by_username(username)

    if user.role_id == 1:
        await app_settings.database.update_additional_teacher_info(username=username, additional_info=additional_info)
    else:
        await app_settings.database.update_additional_student_info(username=username, additional_info=additional_info)

    return {"msg": "Success"}


@router.post("/add-new-groups", tags=["protected"])
async def add_new_groups(request: Request, text_with_groups: TextWithGroups, token: str = Depends(get_token_from_cookie)):
    username = get_username_by_jwt(token)

    user = await app_settings.database.get_user_by_username(username)
    teacher = await app_settings.database.get_teacher_by_username(username)

    if user.role_id != 1:
        return HTTPException(status_code=403, detail="Authorization failed")

    student_groups = text_with_groups.text_with_groups.split("\n")
    student_groups = [group.replace(" ", "").upper() for group in student_groups]

    existing_groups = await app_settings.database.get_all_groups()
    existing_groups = set([group.name for group in existing_groups])

    for group_name in student_groups:
        if group_name in existing_groups:
            continue
        existing_groups.add(group_name)
        group = StudentGroup(name=group_name, teacher_id=teacher.id)
        await app_settings.database.add_group(group=group)

    return {"msg": "Success"}