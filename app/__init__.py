from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    try:
        app.config.from_object(config[config_name])
    except Exception as e:
        print(e)
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap = Bootstrap(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    from .utils import utils as utils_blueprint

    app.register_blueprint(utils_blueprint)

    return app
