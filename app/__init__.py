import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(instance_path: str = 'instance') -> Flask:
    instance_path = os.path.abspath(instance_path)
    app = Flask(__name__, instance_path=instance_path)

    config = Config(instance_path)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # blueprints register
    from .api.task_api import task_api

    app.register_blueprint(task_api, url_prefix='/api/tasks')

    return app
