import logging
import os

from src.datamodels.configs import Config
from src.utils.constants import REMOTE_ENV, LOCAL_ENV


logger = logging.getLogger(__name__)


def init_app_config(env_mode: str, app_config: Config):
    app_config.mode = env_mode
    app_config.worker_timeout = 300
    app_config.routes_timeout = 60
    app_config.host = "[::]"
    app_config.port = 80

    if env_mode == REMOTE_ENV:
        app_config.max_requests = 500
        app_config.workers = 1
        app_config.log_path = "/linal_logs"
        app_config.template_path = "/templates"
    elif env_mode == LOCAL_ENV:
        app_config.max_requests = 100
        app_config.workers = 1
        app_config.log_path = os.path.expanduser("~/linal_logs/")
        app_config.template_path = os.path.expanduser("~/github_projects/LinalEducation/templates")
    else:
        raise RuntimeError(f"Unexpected APPLICATION_ENV value {env_mode}. Use {REMOTE_ENV} or {LOCAL_ENV}.")

    logger.debug(f"Using application config: {app_config}")
