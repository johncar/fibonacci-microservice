import uuid

# import the core functions that defines the business logic
from app.core import fibonacci
import app


class QueueManager(object):
    def __init__(self):
        self.results = {}
        self.available_tasks = {
            'fibonacci': fibonacci
            # add other tasks here
        }

    def start_task(self, name, *args, **kwargs):
        # generate unique id
        task_id = uuid.uuid4().hex

        # execute the task as non-blocking Event
        event = app.start_celery_task.delay(self.available_tasks, name, args, kwargs)

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

