import pytest
from flask_migrate import upgrade

from app import create_app, db
from app.models.task import Task


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('instance', testing=True)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.drop_all()
    db.create_all()
    upgrade()

    task1 = Task(title='Task 1', description='Description 1', done=True)
    task2 = Task(title='Task 2', description='Description 2', done=False)

    db.session.add(task1)
    db.session.add(task2)

    db.session.commit()

    yield db

    db.session.remove()
