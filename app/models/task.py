from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    id_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    def __init__(self, title, done=False):
        self.title = title
        self.done = done

    def __repr__(self) -> str:
        return f'<Task {self.title}>'
