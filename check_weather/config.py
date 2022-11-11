"""This module provides the Check Weather config functionality."""

import configparser
from pathlib import Path

import typer

from check_weather import (
    __app_name__,
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    FILE_WRITE_ERROR,
)


CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / 'config.ini'


def init_app(api_key: str) -> int:
    """
    Initialize the application
    """
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code

    file_code = _create_config_file(api_key)
    if file_code != SUCCESS:
        return file_code

    return SUCCESS


def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR

    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR

    return SUCCESS


def _create_config_file(api_key: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser['openweather'] = {'api_key': api_key}

    try:
        with CONFIG_FILE_PATH.open('w') as file:
            config_parser.write(file)
    except OSError:
        return FILE_WRITE_ERROR

    return SUCCESS