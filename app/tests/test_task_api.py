def test_get_tasks(test_client, init_database):
    response = test_client.get('/api/tasks/')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['title'] == 'Task 1'
    assert response.json[1]['title'] == 'Task 2'


def test_get_task(test_client, init_database):
    response = test_client.get('/api/tasks/1')
    assert response.status_code == 200
    assert response.json['title'] == 'Task 1'

    response = test_client.get('/api/tasks/3')
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found'


def test_get_completed_tasks(test_client, init_database):
    response = test_client.get('/api/tasks/completed')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == 'Task 1'
    assert response.json[0]['done'] == True


def test_get_pending_tasks(test_client, init_database):
    response = test_client.get('/api/tasks/pending')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == 'Task 2'
    assert response.json[0]['done'] == False


def test_create_task(test_client, init_database):
    response = test_client.post(
        '/api/tasks/',
        json={
            'title': 'Task 3',
            'description': 'Description 3',
            'done': False,
        },
    )
    assert response.status_code == 201
    assert response.json['title'] == 'Task 3'
    assert response.json['description'] == 'Description 3'
    assert response.json['done'] == False

    response = test_client.post('/api/tasks/', json={})
    assert response.status_code == 400
    assert response.json['error'] == 'No data provided'

    response = test_client.post('/api/tasks/', json={'title': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Title is required and cannot be empty'


def test_update_task(test_client, init_database):
    response = test_client.patch(
        '/api/tasks/1',
        json={
            'title': 'Task 1 Updated',
            'description': 'Description 1 Updated',
            'done': True,
        },
    )
    assert response.status_code == 200
    assert response.json['title'] == 'Task 1 Updated'
    assert response.json['description'] == 'Description 1 Updated'
    assert response.json['done'] == True

    response = test_client.patch('/api/tasks/3', json={})
    assert response.status_code == 400
    assert response.json['error'] == 'No data provided'

    response = test_client.patch('/api/tasks/3', json={'title': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Title is required and cannot be empty'

    response = test_client.patch('/api/tasks/4', json={'title': 'Task 4'})
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found or error updating task'


def test_delete_task(test_client, init_database):
    response = test_client.delete('/api/tasks/1')
    assert response.status_code == 204

    response = test_client.delete('/api/tasks/4')
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found or error deleting task'
