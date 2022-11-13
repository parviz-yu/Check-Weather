"""An entry-point script to run the app"""

from check_weather import __app_name__, cli_handlers

def main():
    cli_handlers.app(prog_name=__app_name__)


if __name__ == '__main__':
    main()