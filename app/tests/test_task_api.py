def test_get_tasks(test_client, init_database):
    response = test_client.get('/api/tasks/')
    assert response.status_code == 200
    assert len(response.json) == 4
    assert response.json['tasks'][0]['title'] == 'Task 1'
    assert response.json['tasks'][1]['title'] == 'Task 2'

    # Add more tasks to test the done filter
    test_client.post(
        '/api/tasks/',
        json={'title': 'Task 3', 'description': 'Description 3', 'done': True}
    )
    test_client.post(
        '/api/tasks/',
        json={'title': 'Task 4', 'description': 'Description 4', 'done': False}
    )

    # Filter completed tasks
    response = test_client.get('/api/tasks/?done=true')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 2
    assert response.json['tasks'][0]['title'] == 'Task 1'
    assert response.json['tasks'][1]['title'] == 'Task 3'
    assert response.json['total'] == 2
    assert response.json['page'] == 1
    assert response.json['items'] == 2

    # Filter pending tasks
    response = test_client.get('/api/tasks/?done=false')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 2
    assert response.json['tasks'][0]['title'] == 'Task 2'
    assert response.json['tasks'][1]['title'] == 'Task 4'
    assert response.json['total'] == 2
    assert response.json['page'] == 1
    assert response.json['items'] == 2

    # Add more tasks to test pagination
    for i in range(5, 13):
        test_client.post(
            '/api/tasks/',
            json={
                'title': f'Task {i}',
                'description': f'Description {i}',
                'done': False
            })

    # Page 1, 5 tasks per page
    response = test_client.get('/api/tasks/?page=1&per_page=5')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 5
    assert response.json['tasks'][0]['title'] == 'Task 1'
    assert response.json['tasks'][4]['title'] == 'Task 5'
    assert response.json['total'] == 12
    assert response.json['page'] == 1
    assert response.json['items'] == 5

    # Page 2, 5 tasks per page
    response = test_client.get('/api/tasks/?page=2&per_page=5')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 5
    assert response.json['tasks'][0]['title'] == 'Task 6'
    assert response.json['tasks'][4]['title'] == 'Task 10'
    assert response.json['total'] == 12
    assert response.json['page'] == 2
    assert response.json['items'] == 5

    # Page 3, 5 tasks per page (last partial page)
    response = test_client.get('/api/tasks/?page=3&per_page=5')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 2
    assert response.json['tasks'][0]['title'] == 'Task 11'
    assert response.json['tasks'][1]['title'] == 'Task 12'
    assert response.json['total'] == 12
    assert response.json['page'] == 3
    assert response.json['items'] == 2

    # Page out of range
    response = test_client.get('/api/tasks/?page=4&per_page=5')
    assert response.status_code == 404
    assert response.json['error'] == 'Page out of range'


def test_get_task(test_client, init_database):
    response = test_client.get('/api/tasks/1')
    assert response.status_code == 200
    assert response.json['title'] == 'Task 1'

    response = test_client.get('/api/tasks/14')
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found'


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

    response = test_client.patch('/api/tasks/14', json={'title': 'Task 4'})
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found or error updating task'


def test_delete_task(test_client, init_database):
    response = test_client.delete('/api/tasks/1')
    assert response.status_code == 200

    response = test_client.delete('/api/tasks/14')
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found or error deleting task'
