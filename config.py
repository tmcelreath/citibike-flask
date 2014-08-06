""" Environemnt-specific configuration properties """
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Base configuration """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRETKEY'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ Dev config """
    DEBUG = True
    SECRET_KEY = 'ADMIN'
    DEBUG_TB_PANELS = (
        'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel'
        'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
        'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
        'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel'
    )


class TestingConfig(Config):
    """ Test config """
    TESTING = True


class ProductionConfig(Config):
    """ Prod config """
    pass


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
