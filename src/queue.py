import uuid
import multiprocessing
from celery import Celery

# import the core functions that defines the business logic
from core import fibonacci

# app = celery.Celery()
# app.config_from_object('celery_app.celeryconfig')

service_name = 'MathService'
celery = Celery(service_name, backend='rpc://', broker='amqp://guest@localhost//')


@celery.task
def start_task(self, name, args, kwargs):

    # get the named task
    task = self.tasks.get(name)

    # execute it in a
    return lambda: task(*args, **kwargs)


class QueueManager(object):

    def __init__(self):
        self.results = {}
        self.tasks = {
            'fibonacci': fibonacci
            # add other tasks here
        }

    def start_task(self, name, *args, **kwargs):
        # generate unique id
        task_id = uuid.uuid4().hex

        # execute the task as non-blocking Event
        event = start_task.delay(self, name, args, kwargs)

        # store the Event and return the task's unique id to the caller
        self.results[task_id] = event

        return task_id

    def get_result(self, task_id):
        # get the result Event for `task_id`
        result = self.results.get(task_id)

        if result is None:
            return "missing"

        return result.state

    def get_tasks(self):
        return dict(map(lambda (task_id, event): (task_id, self.get_result(task_id)), self.results.iteritems()))


class WorkerProcess(multiprocessing.Process):
    def __init__(self):
        super(WorkerProcess, self).__init__(name='celery_worker_process')

    def run(self):
        argv = [
            'worker',
            '--loglevel=WARNING',
            '--hostname=local',
        ]
        celery.worker_main(argv)

    @staticmethod
    def start_celery():
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

