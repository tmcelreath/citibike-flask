""" App initialization """
from flask import Flask, g
from flask.ext.bootstrap import Bootstrap
from config import config
from flask.ext.pymongo import PyMongo
import logging
from citibike_dao import CitiBikeDAO

bootstrap = Bootstrap()

LOG_FILENAME = 'app.main.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def create_app(config_name):
    """ Factory function for creating application instances
        :param config_name:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo = PyMongo(app)


    @app.before_request
    def connect_db():
        g.dao = CitiBikeDAO(mongo)
        g.mongo = mongo.db
        g.logging = logging

    bootstrap.init_app(app)

    from main import main as main_blueprint
    from api import api as api_blueprint

    app.register_blueprint(main_blueprint, url_prefix='')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
