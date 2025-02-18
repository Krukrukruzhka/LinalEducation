import logging

from fastapi.templating import Jinja2Templates
from src.datamodels.application import ApplicationSettings


logger = logging.getLogger(__name__)
app_settings = ApplicationSettings()


async def activate_application_settings(env_mode: str):
    app_settings.ui.templates = Jinja2Templates(directory=app_settings.app_config.template_path)
    await app_settings.database.create_pool()
    await app_settings.database.setup_tables()

async def deactivate_application_settings():
    # close all connections
    pass
