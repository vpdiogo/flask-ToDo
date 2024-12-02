from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from app.services.task_service import TaskService
from app.utils.response import json_response
from app.utils.logger import get_logger

task_api = Blueprint('task_api', __name__, url_prefix='/api/tasks')
logger = get_logger(__name__)


@task_api.route('/', methods=['GET'])
def get_tasks():
    logger.info('Fetching all tasks')
    try:
        tasks = TaskService.get_all_tasks()
    except Exception as e:
        logger.error(f'Error fetching tasks: {e}')
        return json_response({'error': 'Error fetching tasks'}, status=500)
    return json_response([task.to_dict() for task in tasks], status=200)


@task_api.route('/completed', methods=['GET'])
def get_completed_tasks():
    logger.info('Fetching completed tasks')
    try:
        tasks = TaskService.get_completed_tasks()
    except Exception as e:
        logger.error(f'Error fetching completed tasks: {e}')
        return json_response({'error': 'Error fetching completed tasks'}, status=500)
    return json_response([task.to_dict() for task in tasks], status=200)


@task_api.route('/pending', methods=['GET'])
def get_pending_tasks():
    logger.info('Fetching pending tasks')
    try:
        tasks = TaskService.get_pending_tasks()
    except Exception as e:
        logger.error(f'Error fetching pending tasks: {e}')
        return json_response({'error': 'Error fetching pending tasks'}, status=500)
    return json_response([task.to_dict() for task in tasks], status=200)


@task_api.route('/<int:id>', methods=['GET'])
def get_task(id: int):
    logger.info(f'Fetching task with ID {id}')
    try:
        task = TaskService.get_task_by_id(id)
        if task is None:
            logger.warning(f'Task with ID {id} not found')
            return json_response({'error': 'Task not found'}, status=404)
        return json_response(task.to_dict(), status=200)
    except Exception as e:
        logger.error(f'Error fetching task with ID {id}: {e}')
        return json_response({'error': 'Error fetching task'}, status=500)


@task_api.route('/', methods=['POST'])
def create_task():
    logger.info('Creating a new task')
    try:
        data = request.get_json()
    except BadRequest as e:
        logger.warning(f'Invalid JSON: {e}')
        return json_response({'error': 'Invalid JSON'}, status=400)
    if not data:
        logger.warning('No data provided')
        return json_response({'error': 'No data provided'}, status=400)
    if not data.get('title', '').strip():
        logger.warning('Title is required and cannot be empty')
        return json_response(
            {'error': 'Title is required and cannot be empty'}, status=400
        )
    try:
        task = TaskService.create_task(data)
        if task is None:
            raise Exception('Error creating task')
        return json_response(task.to_dict(), status=201)
    except Exception as e:
        logger.error(f'Error creating task: {e}')
        return json_response({'error': 'Error creating task'}, status=500)


@task_api.route('/<int:task_id>', methods=['PATCH'])
def update_task(task_id: int):
    logger.info(f'Updating task with ID {task_id}')
    try:
        data = request.get_json()
    except BadRequest as e:
        logger.warning(f'Invalid JSON: {e}')
        return json_response({'error': 'Invalid JSON'}, status=400)
    if not data:
        logger.warning('No data provided')
        return json_response({'error': 'No data provided'}, status=400)
    if 'title' not in data or not data['title'].strip():
        logger.warning('Title is required and cannot be empty')
        return json_response(
            {'error': 'Title is required and cannot be empty'}, status=400
        )
    try:
        task = TaskService.update_task(task_id, data)
        if task is None:
            return json_response({'error': 'Task not found or error updating task'}, status=404)
        return json_response(task.to_dict(), status=200)
    except Exception as e:
        logger.error(f'Error updating task with ID {task_id}: {e}')
        return json_response({'error': 'Error updating task'}, status=500)


@task_api.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    logger.info(f'Deleting task with ID {task_id}')
    task = TaskService.delete_task(task_id)
    if task is None:
        logger.warning('Task not found or error deleting task')
        return json_response(
            {'error': 'Task not found or error deleting task'}, status=404
        )
    return json_response({'message': 'Task deleted successfully'}, status=200)
