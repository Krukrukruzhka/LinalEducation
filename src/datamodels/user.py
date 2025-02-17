from typing import Optional
from pydantic import BaseModel

from src.datamodels.utils import StudentMark


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
    marks: list[StudentMark]


class StudentGroup(BaseModel):
    id: Optional[int] = None
    name: str
    teacher_id: int


class UserRole(BaseModel):
    id: Optional[int] = None
    name: str
    ru_name: str


class RolesEnum:
    TEACHER = UserRole(id=1, name="teacher", ru_name="Преподаватель")
    STUDENT = UserRole(id=2, name="student", ru_name="Студент")
    LEADER = UserRole(id=3, name="leader", ru_name="Староста")
    DEVELOPER = UserRole(id=4, name="developer", ru_name="Разработчик")

    ALL = [
        TEACHER,
        STUDENT,
        LEADER,
        DEVELOPER
    ]

    @classmethod
    def get_role_ru_name_by_id(cls, role_id: int) -> Optional[str]:
        for role in cls.ALL:
            if role.id == role_id:
                return role.ru_name
        return None
