from flask import Flask
from .config import CONFIG_VARS


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
            CONFIG_VARS['DB_USER'],
            CONFIG_VARS['DB_PW'],
            CONFIG_VARS['DB_HOST'],
            CONFIG_VARS['DB_NAME']
        )
    app.config['SECRET_KEY'] = CONFIG_VARS['SECRET_KEY']
    app.config['DEBUG'] = True if CONFIG_VARS['DEBUG'] in (True, 'True') else False

    return app
