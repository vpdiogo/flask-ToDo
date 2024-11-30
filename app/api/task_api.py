from flask import Blueprint, jsonify, request

from app.services.task_service import TaskService

task_api = Blueprint('task_api', __name__, url_prefix='/api/tasks')


@task_api.route('/', methods=['GET'])
def get_tasks():
    tasks = TaskService.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200


@task_api.route('/<int:id>', methods=['GET'])
def get_task(id):
    task = TaskService.get_task_by_id(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200


@task_api.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'title' not in data or not data['title'].strip():
        return jsonify({'error': 'Title is required and cannot be empty'}), 400
    task = TaskService.create_task(data)
    return jsonify(task.to_dict()), 201


@task_api.route('/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    task = TaskService.update_task(task_id, data)
    if task is None:
        return jsonify({'error': 'Task not found or error updating task'}), 404
    return jsonify(task.to_dict()), 200


@task_api.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = TaskService.delete_task(task_id)
    if task is None:
        return jsonify({'error': 'Task not found or error deleting task'}), 404
    return '', 204
