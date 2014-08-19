""" App initialization """
from flask import Flask, g
from flask.ext.bootstrap import Bootstrap
from config import config
from pymongo import MongoClient
import logging

bootstrap = Bootstrap()

mongo = MongoClient('localhost', 27017)

LOG_FILENAME = 'app.main.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def create_app(config_name):
    """ Factory function for creating application instances """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.before_request
    def connect_db():
        g.mongo = mongo
        g.logging = logging

    bootstrap.init_app(app)

    from main import main as main_blueprint
    from api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
