from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

from src.datamodels.configs import Config
from database_pg.database import Database


class UISettings(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    templates: Jinja2Templates = None


class ApplicationSettings:
    app_config = Config()
    ui = UISettings()
    database = Database()
