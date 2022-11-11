"""This module provides the Weather Check CLI."""


import typer

from check_weather import ERRORS, api_req, config


app = typer.Typer()


@app.command()
def init() -> None:
    """Initialize the OpenWeather API key"""
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

    typer.secho(f"Congratulations, your API key is valid! Now you can use this app :)", fg=typer.colors.GREEN)
