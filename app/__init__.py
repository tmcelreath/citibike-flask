""" App initialization """
import logging
from flask import Flask, g
from flask.ext.bootstrap import Bootstrap
from flask.ext.pymongo import PyMongo
from flask_limiter import Limiter
from flask_debugtoolbar import DebugToolbarExtension
from config import config
from citibike_dao import CitiBikeDAO

LOG_FILENAME = 'app.main.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

mongo = PyMongo()
bootstrap = Bootstrap()
limiter = Limiter()

def get_mongo():
    return mongo

def create_app(config_name):
    """ Factory function for creating application instances
        :param config_name:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    DEBUG_TOOLBAR = DebugToolbarExtension(app)

    mongo.init_app(app)
    bootstrap.init_app(app)
    limiter.init_app(app)

    @app.before_request
    def pre_request():
        g.dao = CitiBikeDAO(mongo)
        g.mongo = mongo.db
        g.logging = logging

    from main import main as main_blueprint
    from api import api as api_blueprint

    limiter.limit('30/minute')(main_blueprint)
    limiter.limit('100/minute')(api_blueprint)

    app.register_blueprint(main_blueprint, url_prefix='')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
