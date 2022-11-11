import configparser
import json
from typing import Any, NamedTuple
from pathlib import Path

import requests


from check_weather import (
    SUCCESS,
    API_KEY_ERROR,
    CONNECTION_ERROR,
    FILE_STRUCTURE_ERROR,
    SERVER_ERROR,
    JSON_ERROR
)


BASE_WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5'


def check_api_key(api_key: str) -> int:
    params = {'q': 'London', 'appid': api_key}

    try:
        response = requests.get(BASE_WEATHER_API_URL +
                                '/current', params=params)
    except requests.ConnectionError:
        return CONNECTION_ERROR

    if response.status_code == 401:
        return API_KEY_ERROR
    elif response.status_code == 200:
        return SUCCESS
    elif response.status_code >= 500:
        return SERVER_ERROR


def get_api_key(config_file_path: Path) -> str:
    """Return OpenWeather API key"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)
    try:
        return config_parser['openweather']['api_key']
    except KeyError:
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
                return ApiResponse(response.json(), SUCCESS)
            except json.JSONDecodeError:
                return ApiResponse([], JSON_ERROR)

        except requests.ConnectionError:
            return ApiResponse([], CONNECTION_ERROR)