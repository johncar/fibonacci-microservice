import os

from flask import Flask
from celery import Celery

from config import config, Config
from queue import QueueManager
from api import main

conf = config[os.getenv('CONFIG_NAME') or 'default']

celery = Celery(conf.CELERY_APP_NAME, broker=conf.CELERY_BROKER_URL)
celery.config_from_object(conf)


@celery.task
def start_celery_task(available_tasks, name, args, kwargs):
    # get the named task
    task = available_tasks.get(name)

    # execute it in a
    return task(*args, **kwargs)

queue_manager = QueueManager()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object("app.config")
app.register_blueprint(main)
