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

    
    def current(self, city: list[str], imperial: bool) -> MeteorElems:
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


    def daily(self, city: list[str], imperial: bool) -> list[MeteorElems]:
        """Get daily weather forecast from OpenWeather API."""

        city_str = ' '.join(city)
        response = self.handler.make_request(
            'forecast', city_str, imperial
        )

        daily_forecasts = []

        if response.error in ERRORS:
            return [MeteorElems(response.error)]
        else:
            items = response.forecast['list']
            hourly_temp = []
            for i in range(len(items) - 1):
                hourly_temp.append(items[i]['main']['temp'])
                next_hour = datetime.strptime(
                    items[i + 1]['dt_txt'], "%Y-%m-%d %H:%M:%S"
                    ).hour

                # Checks whether the next timestamp is a new day
                # or the end of the list 
                if next_hour == 0 or (len(items) - 2) == i:
                    mean_temp = sum(hourly_temp) / len(hourly_temp)
                    daily_forecasts.append(
                        MeteorElems(
                        0,
                        str(datetime.utcfromtimestamp(items[i]['dt']).date()),
                        city_str.title(),
                        items[i]['weather'][0]['description'],
                        mean_temp, items[i]['main']['humidity'],
                        items[i]['wind']['speed'], items[i]['visibility']
                        )
                    )
                    hourly_temp = []
                
            return daily_forecasts