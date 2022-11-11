import requests


from check_weather import (
    SUCCESS,
    API_KEY_ERROR,
    CONNECTION_ERROR,
    SERVER_ERROR
)


BASE_WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5'



def check_api_key(api_key: str) -> int:
    params = {'q': 'London', 'appid': api_key}

    try:
        response = requests.get(BASE_WEATHER_API_URL + '/current', params=params)
    except requests.ConnectionError:
        return CONNECTION_ERROR

    if response.status_code == 401:
        return API_KEY_ERROR
    elif response.status_code == 200:
        return SUCCESS
    elif response.status_code >= 500:
        return SERVER_ERROR
