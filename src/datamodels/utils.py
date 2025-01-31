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


class AdditionalUserInfo(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    group_name: Optional[str] = None


class StudentWithResults(BaseModel):
    name: str
    total_result: int
    marks: list[bool]


class TextWithGroups(BaseModel):
    text_with_groups: str
