import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cors = CORS()

def create_app(config=None, script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    if config:
        app.config.from_object(config)
    else:
        app_settings = os.getenv("APP_SETTINGS")
        app.config.from_object(app_settings)

        database_url = os.getenv('DATABASE_URL')
        if database_url is not None and database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    # set up extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    # register api
    from src.api import api
    api.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
