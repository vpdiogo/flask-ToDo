import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(
    instance_path: str = 'instance', testing: bool = False
) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        instance_path (str): The path to the instance folder. Defaults to
                             'instance'.
        testing (bool): Flag to indicate if the app is in testing mode.
                        Defaults to False.

    Returns:
        Flask: The configured Flask application instance.
    """
    instance_path = os.path.abspath(instance_path)
    app = Flask(__name__, instance_path=instance_path)

    app_config = Config(instance_path, testing=testing)
    app.config.from_object(app_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # blueprints register
    from .api.task_api import task_api

    app.register_blueprint(task_api, url_prefix='/api/tasks')

    return app
