

"""Top-level package for Check Weather."""


__app_name__ = 'check_weather'
__version__ = '0.1.0'


(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    FILE_STRUCTURE_ERROR,
    FILE_WRITE_ERROR,
    CONNECTION_ERROR,
    API_KEY_ERROR,
    LIMIT_ERROR,
    SERVER_ERROR,
    JSON_ERROR
) = range(10)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    FILE_STRUCTURE_ERROR: "config file structure error",
    FILE_WRITE_ERROR: "config file write error",
    CONNECTION_ERROR: "connection error",
    API_KEY_ERROR: "api key error",
    LIMIT_ERROR: "request limit error",
    SERVER_ERROR: "server error",
}