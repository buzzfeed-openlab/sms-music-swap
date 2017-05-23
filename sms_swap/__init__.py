from flask import Flask
from .app_config import DB_USER, DB_PW, DB_HOST, DB_NAME


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USER, DB_PW, DB_HOST, DB_NAME)
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 240

    return app
