"""This module provides the Weather Check CLI."""


import typer

from check_weather import ERRORS, api_req, config, weather


app = typer.Typer()


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


