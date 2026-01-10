from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app import models
from app.api import deps
import pytest
import numpy as np
import uuid

client = TestClient(app)

def test_attendance_endpoint_exists():
    """Test that POST /attendance endpoint exists."""
    response = client.post(f"{settings.API_V1_STR}/attendance/", json={})
    assert response.status_code != 404

def test_attendance_submission_requires_auth():
    """Test that POST /attendance requires authentication."""
    data = {
        "type": "CLOCK_IN",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "snapshot_base64": "some_base64_string"
    }
    response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
    assert response.status_code == 401

class MockUser:
    def __init__(self):
        self.id = uuid.uuid4()
        self.full_name = "Test User"
        self.branch = MockBranch()
        self.attendance_logs = []

class MockBranch:
    def __init__(self):
        self.name = "Test Branch"
        self.latitude = 14.5995
        self.longitude = 120.9842
        self.radius_meters = 100.0

@pytest.fixture
def mock_user():
    return MockUser()

@pytest.fixture
def mock_face_service(mocker):
    return mocker.patch("app.api.v1.endpoints.attendance.face_service")

@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()

def test_attendance_submission_success(mock_user, mock_face_service, mock_db, mocker):
    """Test successful attendance submission."""
    # Mock face service
    mock_face_service.verify_against_encrypted_storage.return_value = (True, 0.1)
    
    # Mock DB query for face encodings
    mock_encoding_record = mocker.Mock()
    mock_encoding_record.encoding = b"some_encrypted_bytes"
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_encoding_record]
    
    # Mock models.AttendanceLog to have id and timestamp (normally from DB)
    from datetime import datetime
    original_attendance_log = models.AttendanceLog
    def mock_attendance_log_init(*args, **kwargs):
        obj = original_attendance_log(*args, **kwargs)
        obj.id = uuid.uuid4()
        obj.timestamp = datetime.now()
        return obj
    mocker.patch("app.api.v1.endpoints.attendance.models.AttendanceLog", side_effect=mock_attendance_log_init)

    data = {
        "type": "CLOCK_IN",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "snapshot_base64": "some_base64_string"
    }
    
    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 200
        res_data = response.json()
        assert res_data["location_verified"] is True
        assert res_data["type"] == "CLOCK_IN"
    finally:
        app.dependency_overrides.clear()

def test_attendance_submission_no_face(mock_user, mock_face_service, mock_db, mocker):
    """Test submission with no face detected."""
    mock_face_service.verify_against_encrypted_storage.side_effect = ValueError("No face detected in image")
    
    # Mock DB query for face encodings (must have at least one to reach verification)
    mock_encoding_record = mocker.Mock()
    mock_encoding_record.encoding = b"some_encrypted_bytes"
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_encoding_record]
    
    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    data = {
        "type": "CLOCK_IN",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "snapshot_base64": "some_base64_string"
    }
    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 400
        assert "No face detected" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_attendance_submission_face_mismatch(mock_user, mock_face_service, mock_db, mocker):
    """Test submission with face mismatch."""
    mock_face_service.verify_against_encrypted_storage.return_value = (False, 0.6)
    
    mock_encoding_record = mocker.Mock()
    mock_encoding_record.encoding = b"some_encrypted_bytes"
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_encoding_record]
    
    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    data = {
        "type": "CLOCK_IN",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "snapshot_base64": "some_base64_string"
    }
    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 401
        assert "Face verification failed" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_attendance_submission_location_mismatch(mock_user, mock_face_service, mock_db, mocker):
    """Test submission with location outside radius."""
    mock_face_service.verify_against_encrypted_storage.return_value = (True, 0.1)
    
    mock_encoding_record = mocker.Mock()
    mock_encoding_record.encoding = b"some_encrypted_bytes"
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_encoding_record]
    
    # Mock models.AttendanceLog to have id and timestamp (normally from DB)
    from datetime import datetime
    original_attendance_log = models.AttendanceLog
    def mock_attendance_log_init(*args, **kwargs):
        obj = original_attendance_log(*args, **kwargs)
        obj.id = uuid.uuid4()
        obj.timestamp = datetime.now()
        return obj
    mocker.patch("app.api.v1.endpoints.attendance.models.AttendanceLog", side_effect=mock_attendance_log_init)

    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    # Way outside radius (far from Manila)
    data = {
        "type": "CLOCK_IN",
        "latitude": 0.0,
        "longitude": 0.0,
        "snapshot_base64": "some_base64_string"
    }
    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 403
        assert "outside the allowed area" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
