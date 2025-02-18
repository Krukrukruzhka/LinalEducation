from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    user: str = 'krukrukruzhka'
    password: str = 'password'
    database: str = 'LinalEducation'
    host: str = 'localhost'
    port: str = '5432'
    min_size: str = 20  # Минимальное количество соединений
    max_size: str = 20  # Максимальное количество соединений
