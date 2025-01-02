import os
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from functools import partial

from app.router import main_router
from config.application import activate_application_settings, deactivate_application_settings
from config.application import app_settings
from src.utils.constants import LOCAL_ENV


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan_template(_, env_mode: str):
    await activate_application_settings(env_mode=env_mode)
    yield
    await deactivate_application_settings()


def create_app(
    env_mode: str,
    **kwargs,
):
    lifespan = partial(lifespan_template, env_mode=env_mode)

    app = FastAPI(
        debug=bool(env_mode == LOCAL_ENV),
        title='Linear Algebra',
        lifespan=lifespan,
        redirect_slashes=True,
        **kwargs,
    )

    app.mount('/static', StaticFiles(directory=os.path.join(app_settings.app_config.template_path, 'static')), 'static')

    app.include_router(main_router)

    logger.debug("App created successfull")

    return app
