

class Config:
    def __init__(self):
        pass

    # Celery and Flask
    DEBUG = False
    SECRET_KEY = 'Define a hard secret'

    # Celery config
    CELERY_BROKER_URL = 'amqp://localhost:5672//'
    CELERY_RESULT_BACKEND = ''
    CELERY_APP_NAME = 'SetupService'
    CELERY_LOG_LEVEL = 'WARNING'
    CELERY_HOST_NAME = 'local'
    CELERY_WORKER_NAME = 'setupWorker1.%h'

    # Flask config
    JSON_AS_ASCII = True
    SERVER_NAME = 'localhost'
    SERVER_PORT = 5000
    CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
    CELERY_RESULT_BACKEND = 'amqp'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
