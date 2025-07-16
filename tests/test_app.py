import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Activities' in response.data

def test_register_and_unregister(client):
    # Register for an activity
    response = client.post('/register', json={
        'name': 'Test User',
        'activity': 'Yoga'
    })
    assert response.status_code == 200
    assert b'success' in response.data or b'already registered' in response.data

    # Unregister from the activity
    response = client.post('/unregister', json={
        'name': 'Test User',
        'activity': 'Yoga'
    })
    assert response.status_code == 200
    assert b'success' in response.data or b'not registered' in response.data

def test_invalid_register(client):
    # Missing name
    response = client.post('/register', json={
        'activity': 'Yoga'
    })
    assert response.status_code == 400

    # Missing activity
    response = client.post('/register', json={
        'name': 'Test User'
    })
    assert response.status_code == 400
