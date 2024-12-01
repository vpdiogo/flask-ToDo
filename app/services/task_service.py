from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

from app import db
from app.models.task import Task


class TaskService:
    """
    Service class for handling task-related operations.

    Methods:
    --------
    get_all_tasks():
        Retrieves all tasks from the database.

    get_task_by_id(task_id):
        Retrieves a task by its ID. Returns None if the task is not found or if there
        is a database error.

    create_task(data):
        Creates a new task with the provided data. Returns the created task.

    update_task(task_id, data):
        Updates an existing task with the provided data. Returns the updated task or
        None if the task is not found or if there is a database error.

    delete_task(task_id):
        Deletes a task by its ID. Returns the deleted task or None if the task is not
        found or if there is a database error.
    """

    @staticmethod
    def get_all_tasks() -> List[Task]:
        try:
            return Task.query.all()
        except SQLAlchemyError as e:
            logger.error(f'Error retrieving tasks: {e}')
            return []

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        try:
            return Task.query.get(task_id)
        except SQLAlchemyError as e:
            logger.error(f'Error retrieving task with id {task_id}: {e}')
            return None

    @staticmethod
    def create_task(data: dict) -> Optional[Task]:
        try:
            new_task = Task(
                title=data['title'],
                description=data.get('description', ''),
                done=data.get('done', False),
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task
        except SQLAlchemyError as e:
            logger.error(f'Error creating task: {e}')
            db.session.rollback()
            return None

    @staticmethod
    def update_task(task_id: int, data: dict) -> Optional[Task]:
        try:
            task = Task.query.get(task_id)
            if task is None:
                return None
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.done = data.get('done', task.done)
            task.updated_at = db.func.now()
            db.session.commit()
            return task
        except NotFound:
            return None
        except SQLAlchemyError as e:
            logger.error(f'Error updating task with id {task_id}: {e}')
            db.session.rollback()
            return None

    @staticmethod
    def delete_task(task_id: int) -> Optional[Task]:
        try:
            task = Task.query.get_or_404(task_id)
            db.session.delete(task)
            db.session.commit()
            return task
        except NotFound:
            return None
        except SQLAlchemyError as e:
            logger.error(f'Error deleting task with id {task_id}: {e}')
            db.session.rollback()
            return None
