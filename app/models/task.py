from app import db


class Task(db.Model):
    """
    Represents a task in the ToDo application.

    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        description (str): A brief description of the task.
        done (bool): Indicates whether the task is completed.
        id_deleted (bool): Indicates whether the task is deleted.
        created_at (datetime): The timestamp when the task was created.
        updated_at (datetime): The timestamp when the task was last updated.

    Methods:
        __init__(title, description='', done=False):
            Initializes a new Task instance.

        __repr__() -> str:
            Returns a string representation of the Task instance.

        to_dict() -> dict:
            Converts the Task instance to a dictionary.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    def __init__(
        self,
        title: str,
        description: str = '',
        done: bool = False,
        is_deleted: bool = False,
    ):
        self.title = title
        self.description = description
        self.done = done
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f'<Task {self.id} {self.title}>'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'is_deleted': self.is_deleted,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }
