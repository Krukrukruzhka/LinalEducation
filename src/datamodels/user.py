from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    password: str
    role_id: int


class Teacher(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    user_id: int


class Student(BaseModel):
    id: Optional[int] = None
    group_id: Optional[int] = None
    user_id: int
    marks: list[bool]
