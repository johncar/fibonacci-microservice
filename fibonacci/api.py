import app
from flask import jsonify, request, abort, make_response, Blueprint


main = Blueprint('main', __name__)


# Methods

@main.route('/')
def task_list():
    return jsonify({'status': 'ALIVE'})


@main.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': app.queue_manager.get_tasks()})


@main.route('/fibonacci', methods=['POST'])
def start_task():

    if not request.form or 'n' not in request.form:
        abort(400)

    n = int(request.form['n'])

    if n < 0:
        abort(404)

    task_id = app.queue_manager.start_task("fibonacci", n)

    return jsonify({'task': task_id})


@main.route('/task/<string:task_id>')
def task_result(task_id):
    result = app.queue_manager.get_result(task_id)

    return jsonify({'task': task_id, 'result': result})


# Error handling

@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found HA!'}), 404)


@main.errorhandler(400)
def invalid(error):
    return make_response(jsonify({'error': 'Invalid parameters'}), 400)

