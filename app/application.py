import os
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from functools import partial

from app.router import unprotected_routers
from src.datamodels.configs import Config, ConfigDirStructure
from src.state.application import activate_application_state, deactivate_application_state


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan_with_conf(_, app_config: Config, config_dir: ConfigDirStructure):
    await activate_application_state(app_config, config_dir)
    yield
    await deactivate_application_state()


@asynccontextmanager
async def empty_lifespan(_):
    yield


def create_app(
    app_config: Config,
    config_dir: ConfigDirStructure = None,
    **kwargs,
):
    if config_dir:
        lifespan = partial(lifespan_with_conf, app_config=app_config, config_dir=config_dir)
    else:
        lifespan = empty_lifespan
        logger.warning("App created without config directory")

    app = FastAPI(
        debug=app_config.mode,
        title='Linear Algebra',
        lifespan=lifespan,
        redirect_slashes=True,
        **kwargs,
    )

    app.mount('/static', StaticFiles(directory=os.path.join(app_config.template_path, 'static')), 'static')

    app.include_router(unprotected_routers)

    logger.debug("App created successfull")

    return app
