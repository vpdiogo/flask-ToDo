from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from app import db
from app.models.task import Task


class TaskService:
    @staticmethod
    def get_all_tasks():
        return Task.query.all()

    @staticmethod
    def get_task_by_id(task_id):
        try:
            return Task.query.get_or_404(task_id)
        except NotFound:
            return None
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def create_task(data):
        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            done=data.get('done', False),
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def update_task(task_id, data):
        try:
            task = Task.query.get_or_404(task_id)
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.done = data.get('done', task.done)
            db.session.commit()
            return task
        except NotFound:
            return None
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def delete_task(task_id):
        try:
            task = Task.query.get_or_404(task_id)
            db.session.delete(task)
            db.session.commit()
            return task
        except NotFound:
            return None
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            db.session.rollback()
            return None
