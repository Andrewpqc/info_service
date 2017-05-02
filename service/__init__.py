# -*- coding: utf-8 -*-
from flask import Flask
from celery import Celery
from config import config


def create_app(config_name='default'):
    app = Flask(__name__)
    from api import api
    app.config.from_object(config[config_name])
    app.register_blueprint(api, url_prefix='/api')

    return app


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True  # abc
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = create_app()
