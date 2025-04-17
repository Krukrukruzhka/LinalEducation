import argparse
import logging
import logging.handlers
import os
import sys
from logging import NullHandler
from pathlib import Path
from loguru import logger as loguru_logger

import uvicorn
sys.path = ['C:\\Users\\Lena\\Desktop\\LinalEducation', *sys.path]

from app.application import create_app
from src.utils.arguments_parsing import enrich_parser
from config.configs import Config
from database_pg.database import Database
from config.application import app_settings
from src.utils.constants import LOCAL_ENV, DOCKER_ENV, WINDOWS_ENV, MAX_SIZE_LOG_FILE, COUNT_LOG_FILES
from config.app_config import init_app_config


LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logger = logging.getLogger(__name__)


class LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def configurate_loggers(env_mode: str):
    if env_mode in (LOCAL_ENV, DOCKER_ENV, WINDOWS_ENV):
        terminal_common_handler = LoguruHandler()
    else:
        terminal_common_handler = NullHandler()

    log_dir = app_settings.app_config.log_path
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    file_common_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "log.log"), maxBytes=MAX_SIZE_LOG_FILE, backupCount=COUNT_LOG_FILES)

    file_exception_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "exceptions.log"), maxBytes=MAX_SIZE_LOG_FILE, backupCount=COUNT_LOG_FILES)

    working_loggers = [
        *logging.root.manager.loggerDict.keys(),
        "root",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "uvicorn.asgi"
    ]

    for name in working_loggers:
        logging.getLogger(name).handlers = [terminal_common_handler, file_common_handler]
        logging.getLogger(name).propagate = False

    exception_loggers = {
        "src.middleware.logging"
    }

    for name in exception_loggers:
        logger = logging.getLogger(name)
        logger.handlers = [file_common_handler, file_exception_handler]

def create_parser():
    parser = argparse.ArgumentParser()
    enrich_parser(parser, Config)
    return parser.parse_args()

def start_app():
    args = create_parser()
    env_mode = os.getenv("APPLICATION_ENV", None) or getattr(args, 'mode', None)
    logging.root.setLevel(LOG_LEVEL)

    init_app_config(env_mode=env_mode, app_config=app_settings.app_config, db_config=app_settings.db_config)
    app_settings.database = Database(db_config=app_settings.db_config)

    configurate_loggers(env_mode)

    # Create the application
    app = create_app(env_mode)

    # Run with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80, log_level=LOG_LEVEL.lower())


if __name__ == "__main__":
    start_app()