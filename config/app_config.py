import logging
import os

from config.configs import Config
from config.database_config import DatabaseConfig
from src.utils.constants import REMOTE_ENV, LOCAL_ENV, DOCKER_ENV


logger = logging.getLogger(__name__)


def init_app_config(env_mode: str, app_config: Config, db_config: DatabaseConfig):
    app_config.mode = env_mode
    app_config.worker_timeout = 300
    app_config.routes_timeout = 60
    app_config.host = "[::]"
    app_config.port = 8000
    app_config.workers = 1
    app_config.log_path = "/linal_logs"
    app_config.template_path = "/LinalEducation/templates"

    if env_mode == REMOTE_ENV:
        app_config.max_requests = 500
        app_config.workers = 10
    elif env_mode == LOCAL_ENV:
        app_config.max_requests = 100
        app_config.workers = 1
        app_config.log_path = os.path.expanduser("~/linal_logs/")
        app_config.template_path = os.path.expanduser("~/github_projects/LinalEducation/templates")
        app_config.port = 80
    elif env_mode == DOCKER_ENV:
        db_config.host = "db"
        app_config.max_requests = 100
        app_config.workers = 1
    else:
        raise RuntimeError(f"Unexpected APPLICATION_ENV value {env_mode}. Use {REMOTE_ENV}, {LOCAL_ENV} or {DOCKER_ENV}.")

    logger.debug(f"Using application config: {app_config}")
