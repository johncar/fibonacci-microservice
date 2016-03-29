import os
import multiprocessing

from config import config
from fibonacci import celery

conf = config[os.getenv('CONFIG_NAME') or 'default']


class WorkerProcess(multiprocessing.Process):
    def __init__(self):
        super(WorkerProcess, self).__init__(name='celery_worker_process')

    def run(self):
        argv = [
            'worker',
            '--loglevel=' + conf.CELERY_LOG_LEVEL,
            '--hostname=' + conf.CELERY_HOST_NAME,
            '-n',
            conf.CELERY_WORKER_NAME
        ]
        celery.worker_main(argv)

    @staticmethod
    def start_celery():
        os.system("ps auxww | grep '^celery worker' | awk '{print $2}' | xargs kill -9")

        if worker_process is None:
            global worker_process
            worker_process = WorkerProcess()
            worker_process.start()

    @staticmethod
    def stop_celery():
        global worker_process
        if worker_process:
            worker_process.terminate()
            worker_process = None

worker_process = None
