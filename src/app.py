from flask import Flask, request, jsonify, abort, make_response
from queue import QueueManager, WorkerProcess

app = Flask(__name__)
queue_manager = QueueManager()


# Service endpoints

@app.route('/')
def task_list():
    return jsonify({'status': 'ALIVE'})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': queue_manager.get_tasks()})


@app.route('/fibonacci', methods=['POST'])
def start_task():

    if not request.json or 'number' not in request.json:
        abort(400)

    if type(request.json['number']) != unicode:
        abort(400)

    n = int(request.json['number'])

    task_id = queue_manager.start_task("fibonacci", n)

    return jsonify({'task': task_id})


@app.route('/task/<string:task_id>')
def task_result(task_id):
    result = queue_manager.get_result(task_id)

    return jsonify({'task': task_id, 'result': result})


# Error handlers

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found HA!'}), 404)


@app.errorhandler(400)
def invalid(error):
    return make_response(jsonify({'error': 'Invalid parameters'}), 400)


if __name__ == '__main__':

    WorkerProcess.start_celery()

    app.run(debug=True)
