import pytest
from app import create_app, db, User, UserGroup

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_create_user(client):
    data = {"name": "Test User"}
    response = client.post('/user', json=data)
    assert response.status_code == 201
    assert response.json['name'] == "Test User"

def test_create_group(client):
    data = {"name": "Test Group"}
    response = client.post('/group', json=data)
    assert response.status_code == 201
    assert response.json['name'] == "Test Group"

def test_get_user(client):
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/user/{user.id}')
    assert response.status_code == 200
    assert response.json['name'] == "Test User"

def test_get_group(client):
    group = UserGroup(name="Test Group")
    db.session.add(group)
    db.session.commit()

    response = client.get(f'/group/{group.id}')
    assert response.status_code == 200
    assert response.json['name'] == "Test Group"

def test_get_users(client):
    user1 = User(name="User 1")
    user2 = User(name="User 2")
    db.session.add_all([user1, user2])
    db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_groups(client):
    group1 = UserGroup(name="Group 1")
    group2 = UserGroup(name="Group 2")
    db.session.add_all([group1, group2])
    db.session.commit()

    response = client.get('/groups')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_delete_user(client):
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    response = client.delete(f'/user/{user.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted'

def test_delete_group(client):
    group = UserGroup(name="Test Group")
    db.session.add(group)
    db.session.commit()

    response = client.delete(f'/group/{group.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Group deleted'
