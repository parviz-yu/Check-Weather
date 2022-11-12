"""This Module provides controller for Check Weather app."""


from datetime import datetime
from typing import NamedTuple

from check_weather import api_req, ERRORS


class MeteorElems(NamedTuple):
    """
    Сontainer of meteorological elements.
    """
    
    error: int = 0
    day: str | None = None
    city: str | None = None
    desctiption: str | None = None
    aver_temp: float | int | None = None
    humidity: float | int | None = None
    wind_speed: float | int | None = None
    visibility: float | int | None = None


class Forecast:
    """
    Object connects CLI with the API requests.
    """

    def __init__(self, api_key: str) -> None:
        self.handler = api_req.ApiHandler(api_key)

    
    def current(self, city: list[str], imperial: bool):
        """Get current weather from OpenWeather API."""
        
        joined_str = ' '.join(city)
        response = self.handler.make_request(
            'weather', joined_str, imperial
        )

        if response.error in ERRORS:
            return MeteorElems(response.error)
        else:
            return MeteorElems(
                response.error, str(datetime.now().date()),
                response.forecast['name'],
                response.forecast['weather'][0]['description'],
                response.forecast['main']['temp'],
                response.forecast['main']['humidity'],
                response.forecast['wind']['speed'],
                response.forecast['visibility']
            )
