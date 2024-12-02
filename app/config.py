import os
import json
from typing import Any


class Config:
    """
    Configuration class for loading settings from a JSON file.

    Attributes:
        DEBUG (bool): Indicates if debugging is enabled.
        SQLALCHEMY_DATABASE_URI (str): URI for the SQLAlchemy database.
        SECRET_KEY (str): Secret key for the application.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Indicates if SQLAlchemy should
            track modifications.

    Args:
        path_instance (str): Path to the instance folder containing the
            settings file.
        testing (bool): Flag indicating if the application is in testing mode.

    Raises:
        FileNotFoundError: If the settings file is not found at the specified
            path.
    """

    def __init__(self, path_instance: str, testing: bool) -> None:
        settings_file_path = os.path.join(path_instance, 'settings.json')

        if os.path.exists(settings_file_path):
            with open(settings_file_path) as f:
                config_data: dict[str, Any] = json.load(f)
            self.DEBUG: bool = config_data.get('DEBUG', False)
            self.SQLALCHEMY_DATABASE_URI: str = config_data.get(
                'SQLALCHEMY_DATABASE_URI'
            )
            self.SECRET_KEY: str = config_data.get('SECRET_KEY')
            self.SQLALCHEMY_TRACK_MODIFICATIONS: bool = config_data.get(
                'SQLALCHEMY_TRACK_MODIFICATIONS', False
            )
        else:
            raise FileNotFoundError(
                f'Config file not found at {settings_file_path} in instance '
                f'path {path_instance}'
            )
