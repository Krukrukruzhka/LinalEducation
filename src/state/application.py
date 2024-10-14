import logging
import os
import re
import yaml

from pathlib import Path
from functools import partial

from fastapi.templating import Jinja2Templates

from src.datamodels.application import ApplicationState
from src.datamodels.configs import Config, ConfigDirStructure


PATTERN = re.compile(r'.*?\${(\w+)}.*?')
TAG = '!ENV'

logger = logging.getLogger(__name__)
app_state = ApplicationState()


def _get_loader():
    def constructor_env_variables(loader: yaml.SafeLoader, node):
        value = loader.construct_scalar(node)
        match = PATTERN.findall(value)  # find all env var in line

        if match:
            full_value = value
            for var in match:
                full_value = full_value.replace(
                    f'${{{var}}}', os.environ.get(var, var)
                )
            return full_value

        return value

    loader = yaml.SafeLoader
    loader.add_constructor(TAG, constructor_env_variables)

    return loader


def _read_config(yaml_file_path, config_dir: ConfigDirStructure, loader: yaml.SafeLoader):
    yaml_path = Path(config_dir.path).joinpath(yaml_file_path).read_text()
    return yaml.load(yaml_path, Loader=loader)


async def activate_application_state(app_config: Config, config_dir: ConfigDirStructure):
    read_config = partial(_read_config, config_dir=config_dir, loader=_get_loader())

    app_state.app_config = app_config
    app_state.ui.templates = Jinja2Templates(directory=app_config.template_path)


async def deactivate_application_state():
    # close all connections
    pass
