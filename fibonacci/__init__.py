import os

from flask import Flask
from celery import Celery

from config import config, Config

from socket import error as socket_error

conf = config[os.getenv('CONFIG_NAME') or 'default']

celery = Celery(conf.CELERY_APP_NAME, broker=conf.CELERY_BROKER_URL)
celery.config_from_object(conf)


from api import main
from queue import QueueManager
from worker import WorkerProcess


@celery.task
def start_celery_task(available_tasks, name, args, kwargs):
    # get the named task
    task = available_tasks.get(name)

    # execute it in a
    return task(*args, **kwargs)

queue_manager = QueueManager()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object("fibonacci.config")
app.register_blueprint(main)


def main():
    try:
        WorkerProcess.start_celery()
        app.run(host=conf.SERVER_NAME, port=conf.SERVER_PORT, debug=conf.DEBUG)

    except socket_error, msg:
        print "Caught exception socket.error : %s" % msg

    finally:
        WorkerProcess.stop_celery()
