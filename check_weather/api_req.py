import configparser
import json
from pathlib import Path
from typing import Any, NamedTuple


import requests


from check_weather import (
    SUCCESS,
    API_KEY_ERROR,
    CONNECTION_ERROR,
    FILE_STRUCTURE_ERROR,
    LIMIT_ERROR,
    SERVER_ERROR,
    JSON_ERROR,
    NOT_FOUND_ERROR,
    UNKNOWN_ERROR
)


BASE_WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5'


def check_api_key(api_key: str) -> int:
    params = {'q': 'London', 'appid': api_key}

    try:
        response = requests.get(BASE_WEATHER_API_URL +
                                '/weather', params=params)
    except requests.ConnectionError:
        return CONNECTION_ERROR

    return check_status_code(response)


def check_status_code(response: requests.Response) -> int:
    if response.status_code == 401:
        return API_KEY_ERROR
    elif response.status_code == 404:
        return NOT_FOUND_ERROR
    elif response.status_code == 200:
        return SUCCESS
    elif response.status_code == 429:
        return LIMIT_ERROR
    elif response.status_code >= 500:
        return SERVER_ERROR
    else:
        return UNKNOWN_ERROR


def get_api_key(config_file_path: Path) -> str | int:
    """Return OpenWeather API key"""
    config_parser = configparser.ConfigParser()
    try:
        config_parser.read(config_file_path)
        return config_parser['openweather']['api_key']
    except Exception:
        return FILE_STRUCTURE_ERROR


class ApiResponse(NamedTuple):
    forecast: dict[str, Any]
    error: int


class ApiHandler:
    def __init__(self, api_key: str) -> None:
        self.key = api_key

    def make_request(self, type: str, city: str, units: bool) -> ApiResponse:
        query = {
            'q': city,
            'units': 'metric' if not units else 'imperial',
            'appid': self.key
        }
        type = '/' + type
        try:
            response = requests.get(BASE_WEATHER_API_URL + type, params=query)
            try:
                resp_code = check_status_code(response)
                if resp_code != SUCCESS:
                    return ApiResponse({}, resp_code)
                return ApiResponse(response.json(), SUCCESS)
            except json.JSONDecodeError:
                return ApiResponse({}, JSON_ERROR)
        except requests.ConnectionError:
            return ApiResponse({}, CONNECTION_ERROR)