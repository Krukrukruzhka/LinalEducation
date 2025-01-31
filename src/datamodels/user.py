import enum
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


class StudentGroup(BaseModel):
    id: Optional[int] = None
    name: str
    teacher_id: int


class UserRole(BaseModel):
    id: Optional[int] = None
    name: str
    ru_name: str


class Roles(enum.Enum):
    teacher = UserRole(id=1, name="teacher", ru_name="Преподаватель")
    student = UserRole(id=2, name="student", ru_name="Студент")
    leader = UserRole(id=3, name="leader", ru_name="Староста")
    developer = UserRole(id=4, name="developer", ru_name="Разработчик")

    @classmethod
    def get_role_ru_name_by_id(cls, role_id: int) -> Optional[str]:
        for role in cls:
            if role.value.id == role_id:
                return role.value.ru_name
        return None
