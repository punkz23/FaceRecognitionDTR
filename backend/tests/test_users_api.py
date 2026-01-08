from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.api import deps
import pytest
import numpy as np
import uuid

client = TestClient(app)

class MockUser:
    def __init__(self, id=None):
        self.id = id or uuid.uuid4()
        self.email = "admin@example.com"
        self.is_active = True
        self.role = "admin"

@pytest.fixture
def mock_admin():
    return MockUser()

@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_face_service(mocker):
    return mocker.patch("app.api.v1.endpoints.users.face_service")

@pytest.fixture
def mock_encryption(mocker):
    return mocker.patch("app.api.v1.endpoints.users.DataEncryption")

def test_enroll_face_success(mock_admin, mock_db, mock_face_service, mock_encryption, mocker):
    user_id = str(uuid.uuid4())
    mock_target_user = MockUser(id=user_id)
    
    # Mock DB query for user
    mock_db.query.return_value.filter.return_value.first.return_value = mock_target_user
    
    # Mock face service
    mock_face_service.decode_image.return_value = np.zeros((100, 100, 3))
    mock_face_service.get_face_encodings.return_value = [np.random.rand(128)]
    
    # Mock encryption
    mock_encryption.encrypt.return_value = b"encrypted_bytes"
    
    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    try:
        data = {"image_base64": "fake_base64_data"}
        response = client.post(f"{settings.API_V1_STR}/users/{user_id}/face-enroll", json=data)
        
        assert response.status_code == 200
        assert response.json() == {"message": "Face enrolled successfully"}
        assert mock_db.add.called
        assert mock_db.commit.called
    finally:
        app.dependency_overrides.clear()

def test_enroll_face_no_user(mock_admin, mock_db):
    user_id = str(uuid.uuid4())
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    try:
        data = {"image_base64": "fake_base64_data"}
        response = client.post(f"{settings.API_V1_STR}/users/{user_id}/face-enroll", json=data)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    finally:
        app.dependency_overrides.clear()

def test_enroll_face_no_face_detected(mock_admin, mock_db, mock_face_service):
    user_id = str(uuid.uuid4())
    mock_db.query.return_value.filter.return_value.first.return_value = MockUser(id=user_id)
    
    mock_face_service.decode_image.return_value = np.zeros((100, 100, 3))
    mock_face_service.get_face_encodings.return_value = []
    
    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    try:
        data = {"image_base64": "fake_base64_data"}
        response = client.post(f"{settings.API_V1_STR}/users/{user_id}/face-enroll", json=data)
        assert response.status_code == 400
        assert "No face detected" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_enroll_face_multiple_faces(mock_admin, mock_db, mock_face_service):
    user_id = str(uuid.uuid4())
    mock_db.query.return_value.filter.return_value.first.return_value = MockUser(id=user_id)
    
    mock_face_service.decode_image.return_value = np.zeros((100, 100, 3))
    mock_face_service.get_face_encodings.return_value = [np.random.rand(128), np.random.rand(128)]
    
    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    try:
        data = {"image_base64": "fake_base64_data"}
        response = client.post(f"{settings.API_V1_STR}/users/{user_id}/face-enroll", json=data)
        assert response.status_code == 400
        assert "Multiple faces detected" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
