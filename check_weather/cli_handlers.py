"""This module provides the Weather Check CLI."""


import typer

from check_weather import ERRORS, api_req, config, weather


PD = 18     # Padding
BG = "\033[45m"     # Background color
FONT = "\033[4;35m"     # Font color
RESET = "\033[0m"


app = typer.Typer(
    help="Awesome CLI app for weather checking",
    )


@app.command()
def init() -> None:
    """Initialize the OpenWeather API key."""

    api_key = typer.prompt('Please input OpenWeather API key')

    api_key_check_error = api_req.check_api_key(api_key)
    if api_key_check_error:
        typer.secho(
            f'FAILED with "{ERRORS[api_key_check_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    init_error = config.init_app(api_key)
    if init_error:
        typer.secho(
            f'FAILED with "{ERRORS[init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    typer.secho(
        f"Congratulations, your API key is valid! Now you can use this app :)",
        fg=typer.colors.GREEN
    )


def get_forecast() -> weather.Forecast:
    """
    Helper function

    The function checks the existence of the config file and its structure.
    Stops the program when errors occur.
    Returns "Forecast" object for further interaction with the API.
    """

    if config.CONFIG_FILE_PATH.exists():
        api_key = api_req.get_api_key(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "check_weather init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if isinstance(api_key, str):
        return weather.Forecast(api_key)
    else:
        typer.secho(
            f'FAILED with {ERRORS[api_key]}. Please, run "check_weather init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def today(
    city: list[str] = typer.Argument(
        ..., show_default=False),
    imperial: bool = typer.Option(
        False,
        '-i', '--imperial',
        help='Display the temprature in imperial units.'
    ),
    verbose: bool = typer.Option(
        False,
        '-v', '--verbose',
        help='Display detailed weather forecast.'
    )
) -> None:
    """
    Show today's weather of CITY.
    """

    forecast_answer = get_forecast()
    forecast = forecast_answer.current(city, imperial)

    if forecast.error:
        typer.secho(
            f'FAILED with "{ERRORS[forecast.error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        print(
            f'{BG}{forecast.day:^{PD}}/{forecast.city:^{PD}}{RESET}',
            'Average temperature - '
            f"{FONT}({forecast.aver_temp}°{'F' if imperial else 'C'}){RESET}",
            sep='\n'
        )

        if verbose:
            print(
                f'Weather description: {forecast.desctiption}',
                f'Humidity - {forecast.humidity}%',
                f"Wind speed - {forecast.wind_speed} {'Mph' if imperial else 'M/s'}",
                f'Visibility - {forecast.visibility}', sep="\n"
            )