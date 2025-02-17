from pydantic import BaseModel
from typing import Optional

from src.datamodels.user import User, Teacher, Student, StudentGroup


class BasicData(BaseModel):
    user: User
    role_name: str
    all_groups: list[StudentGroup]

    teacher: Optional[Teacher] = None

    student: Optional[Student] = None
    student_group: Optional[StudentGroup] = None
