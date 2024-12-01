from flask import Blueprint, Response, request

from app.services.task_service import TaskService
from app.utils.response import json_response

task_api = Blueprint('task_api', __name__, url_prefix='/api/tasks')


@task_api.route('/', methods=['GET'])
def get_tasks() -> Response:
    tasks = TaskService.get_all_tasks()
    return json_response([task.to_dict() for task in tasks], status=200)


@task_api.route('/<int:id>', methods=['GET'])
def get_task(id: int) -> Response:
    task = TaskService.get_task_by_id(id)
    if task is None:
        return json_response({'error': 'Task not found'}, status=404)
    return json_response(task.to_dict(), status=200)


@task_api.route('/', methods=['POST'])
def create_task() -> Response:
    data = request.get_json()
    if not data:
        return json_response({'error': 'No data provided'}, status=400)
    if 'title' not in data or not data['title'].strip():
        return json_response(
            {'error': 'Title is required and cannot be empty'}, status=400
        )
    task = TaskService.create_task(data)
    return json_response(task.to_dict(), status=201)


@task_api.route('/<int:task_id>', methods=['PATCH'])
def update_task(task_id: int) -> Response:
    data = request.get_json()
    if not data:
        return json_response({'error': 'No data provided'}, status=400)
    if 'title' not in data or not data['title'].strip():
        return json_response(
            {'error': 'Title is required and cannot be empty'}, status=400
        )
    task = TaskService.update_task(task_id, data)
    if task is None:
        return json_response(
            {'error': 'Task not found or error updating task'}, status=404
        )
    return json_response(task.to_dict(), status=200)


@task_api.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Response:
    task = TaskService.delete_task(task_id)
    if task is None:
        return json_response(
            {'error': 'Task not found or error deleting task'}, status=404
        )
    return json_response({'message': 'Task deleted successfully'}, status=204)
