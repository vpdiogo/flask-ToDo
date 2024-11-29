from flask import Blueprint, jsonify

task_api = Blueprint('task_api', __name__)


@task_api.route('/')
def list_tasks():
    return jsonify({'tasks': []})
