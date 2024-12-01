import os
import json


class Config:
    def __init__(self, path_instance: str, testing: bool) -> None:
        settings_file = os.path.join(path_instance, 'settings.json')

        if os.path.exists(settings_file):
            with open(settings_file) as f:
                config_data: dict = json.load(f)
            self.DEBUG: bool = config_data.get('DEBUG', False)
            self.SQLALCHEMY_DATABASE_URI: str = config_data.get(
                'SQLALCHEMY_DATABASE_URI_TEST' if testing else 'SQLALCHEMY_DATABASE_URI'
            )
            self.SECRET_KEY: str = config_data.get('SECRET_KEY')
            self.SQLALCHEMY_TRACK_MODIFICATIONS: bool = config_data.get(
                'SQLALCHEMY_TRACK_MODIFICATIONS', False
            )
        else:
            raise FileNotFoundError(f'Config file not found: {settings_file}')
