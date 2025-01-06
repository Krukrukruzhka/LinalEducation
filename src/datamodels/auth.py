from pydantic import BaseModel


class RegistrationRequest(BaseModel):
    name: str
    username: str
    role_id: int
    password: str
    repeated_password: str
