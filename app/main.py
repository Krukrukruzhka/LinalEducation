import argparse
import logging
import logging.handlers
import os
import random
import sys
from logging import NullHandler

import gunicorn.app.base as gap
from gunicorn.glogging import Logger
from pathlib import Path
from loguru import logger as loguru_logger

from app.application import create_app
from database_pg.database import Database
from src.utils.arguments_parsing import enrich_parser
from config.configs import Config
from config.application import app_settings
from src.utils.constants import LOCAL_ENV, DOCKER_ENV
from src.utils.constants import MAX_SIZE_LOG_FILE, COUNT_LOG_FILES
from config.app_config import init_app_config


LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logger = logging.getLogger(__name__)


class MainApp(gap.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}

        for key, value in config.items():
            if type(key) is str:
                self.cfg.set(key.lower(), value)
            else:
                logger.exception("Config type is not str")
                raise TypeError

    def load(self):
        return self.application


class GunicorLogger(Logger):
    def setup(self, cfg):
        self.error_logger = logging.getLogger("gunicorn.error")
        self.access_logger = logging.getLogger("gunicorn.access")

        self.error_logger.setLevel(LOG_LEVEL)
        self.access_logger.setLevel(LOG_LEVEL)


class LoguruHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configurate_loggers(env_mode: str):
    if env_mode in (LOCAL_ENV, DOCKER_ENV):
        terminal_common_handler = LoguruHandler()
        file_common_handler = NullHandler()
        file_exception_handler = NullHandler()
    else:
        terminal_common_handler = NullHandler()
        log_dir = app_settings.app_config.log_path
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        file_common_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(log_dir, "log.log"), maxBytes=MAX_SIZE_LOG_FILE, backupCount=COUNT_LOG_FILES)
        file_exception_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(log_dir, "exceptions.log"), maxBytes=MAX_SIZE_LOG_FILE, backupCount=COUNT_LOG_FILES)

    working_loggers = [
        *logging.root.manager.loggerDict.keys(),
        "root",
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]

    for name in working_loggers:
        logging.getLogger(name).handlers = [terminal_common_handler, file_common_handler]
        logging.getLogger(name).propagate = False

    exception_loggers = {
        "src.middleware.logging"
    }

    for name in exception_loggers:
        logging.getLogger(name).handlers = [file_common_handler, file_exception_handler]


def create_parser():
    parser = argparse.ArgumentParser()
    enrich_parser(parser, Config)
    return parser.parse_args()


def start_app():
    args = create_parser()  # arguments from the bash script

    env_mode = os.getenv("APPLICATION_ENV", None) or getattr(args, 'mode', None)
    logging.root.setLevel(LOG_LEVEL)

    init_app_config(env_mode=env_mode, app_config=app_settings.app_config, db_config=app_settings.db_config)
    app_settings.database = Database(db_config=app_settings.db_config)

    configurate_loggers(env_mode=env_mode)
    logger.debug(f"Using args: {args}")

    app = create_app(env_mode=env_mode)

    app_config = app_settings.app_config
    bind = f"{app_config.host}:{app_config.port}" if not getattr(app_config, 'uds', None) else f"unix://{app_config.uds}"
    logger.info(f"Starting server on {bind} in mode {app_config.mode}")

    MainApp(
        app,
        options={
            'bind': bind,
            'workers': app_config.workers,
            'worker_class': app_config.worker_class,
            'logger_class': GunicorLogger,
            'max_requests': app_config.max_requests,
            'max_requests_jitter': random.randint(0, app_config.max_requests//5),
            'timeout': app_config.worker_timeout,
        },
    ).run()


if __name__ == '__main__':
    start_app()
