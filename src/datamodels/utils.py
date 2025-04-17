from pydantic import BaseModel
from typing import Optional


class AdditionalUserInfo(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    group_name: Optional[str] = None


class StudentMark(BaseModel):
    result: bool
    approve_date: Optional[str]


class StudentWithResults(BaseModel):
    name: str
    total_linal_result: int
    total_angem_result: int
    linal_marks: list[StudentMark]
    angem_marks: list[StudentMark]


class TextWithGroups(BaseModel):
    text_with_groups: str
