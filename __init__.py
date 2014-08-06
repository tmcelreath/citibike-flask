from Flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import config
from flask_debugtoolbar import DebugToolbarExtension

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    DEBUG_TOOLBAR = DebugToolbarExtension(app)

    bootstrap.init_app(app)

    if not app.debug and not app.testing:
        from flask.ext.sslify = SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app