from pydantic import BaseModel, Field

from fastapi.templating import Jinja2Templates

from src.datamodels.configs import Config


class UISettings(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    templates: Jinja2Templates = None


class ApplicationSettings(BaseModel):
    app_config: Config = Field(default=Config())
    ui: UISettings = Field(default=UISettings())
