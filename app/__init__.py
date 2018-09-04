import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


def create_app(config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


app = create_app(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import commands
from app import results, models, polls, surveys
