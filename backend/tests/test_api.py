from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.api import deps

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Face Recognition DTR API"}

def test_login_access_token(mocker):
    # Mock the database query to return None (user not found)
    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    try:
        response = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
        # Expect 400 because user doesn't exist
        assert response.status_code == 400
    finally:
        app.dependency_overrides.clear()

def test_create_user_unauthorized(mocker):
    # Mock the database to avoid connection issues
    mock_db = mocker.Mock()
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    # Try to create a user without being admin
    data = {
        "email": "newuser@example.com",
        "password": "password123",
        "employee_id": "EMP001",
        "full_name": "New User"
    }
    try:
        response = client.post(f"{settings.API_V1_STR}/users/", json=data)
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()
