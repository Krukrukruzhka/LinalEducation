import logging
from time import sleep

from fastapi.templating import Jinja2Templates
from src.datamodels.application import ApplicationSettings
from src.utils.constants import DB_RETRY_COUNT, DB_RETRY_SLEEP_SECONDS


logger = logging.getLogger(__name__)
app_settings = ApplicationSettings()


async def activate_application_settings(env_mode: str):
    app_settings.ui.templates = Jinja2Templates(directory=app_settings.app_config.template_path)

    is_created_pools = False
    connect_exception = None

    logger.info("Try connect to database")
    for retry_iteration in range(DB_RETRY_COUNT):
        try:
            logger.info(f"iteration number {retry_iteration}")
            await app_settings.database.create_pool()
            is_created_pools = True
        except Exception as exception:
            connect_exception = exception
            sleep(DB_RETRY_SLEEP_SECONDS)
        if is_created_pools:
            logger.info(f"Successful connected to database")
            break
    if not is_created_pools:
        raise connect_exception

    await app_settings.database.setup_tables()

async def deactivate_application_settings():
    # close all connections
    pass
