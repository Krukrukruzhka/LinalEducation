from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

from config.configs import Config
from config.database_config import DatabaseConfig
from database_pg.database import Database


class UISettings(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    templates: Jinja2Templates = None


class ApplicationSettings:
    app_config = Config()
    ui = UISettings()
    db_config = DatabaseConfig()
    database: Database = None
