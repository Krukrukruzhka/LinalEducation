import argparse
import logging
import logging.handlers
import os
import random
import sys
import yaml

import gunicorn.app.base as gap
from gunicorn.glogging import Logger
from pathlib import Path
from loguru import logger as loguru_logger

from app.application import create_app
from src.utils.arguments_parsing import enrich_parser
from src.datamodels.configs import ConfigDirStructure, Config


LOG_LEVEL_NUMBER = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
MAX_SIZE_LOG_FILE = 20*1024*1024
COUNT_LOG_FILES = 5

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
        handler = logging.NullHandler()  # disable gunicorn logging

        self.error_logger = logging.getLogger("gunicorn.error")
        # self.error_logger.addHandler(handler)
        self.error_logger.setLevel(LOG_LEVEL_NUMBER)

        self.access_logger = logging.getLogger("gunicorn.access")
        # self.access_logger.addHandler(handler)
        self.access_logger.setLevel(LOG_LEVEL_NUMBER)


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


def configurate_loggers(log_dir: str):
    """_summary_

    Args:
        log_dir (str): path to directory with log files

    Logs can be sending to terminal and machine
    """

    terminal_common_handler = LoguruHandler()

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

    app_env = os.getenv("APPLICATION_ENV", None) or getattr(args, 'mode', None)

    logging.root.setLevel(LOG_LEVEL_NUMBER)

    if getattr(args, 'config_dir', None) is not None:
        config_dir = ConfigDirStructure(path=str(Path(args.config_dir).joinpath(app_env.lower())))
        app_config = Config(**yaml.safe_load(Path(config_dir.path).joinpath(config_dir.application).read_text()))
    else:
        logger.debug("conf_dir is None")
        config_dir = None
        app_config = Config(vars(args))

    configurate_loggers(log_dir=app_config.log_path)
    logger.debug(f"Using args: {args}")

    app = create_app(
        app_config=app_config,
        config_dir=config_dir
    )

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
