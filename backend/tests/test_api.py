from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Face Recognition DTR API"}

def test_login_access_token():
    # 1. First, create a user (mocking this part or assuming seed data)
    # For this test environment, we'll try to login with a non-existent user to check 400
    # or we need to setup a test DB. 
    # For simplicity in this script, we check the structure of the call.
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    response = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    # Expect 400 because user doesn't exist in empty DB
    assert response.status_code == 400 

def test_create_user_unauthorized():
    # Try to create a user without being admin
    data = {
        "email": "newuser@example.com",
        "password": "password123",
        "employee_id": "EMP001",
        "full_name": "New User"
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=data)
    assert response.status_code == 401
