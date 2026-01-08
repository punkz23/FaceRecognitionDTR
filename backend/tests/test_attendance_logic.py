from fastapi.testclient import TestClient
from app.main import app
from app.api import deps
from app import models, schemas
from app.core.encryption import DataEncryption
import pytest
import numpy as np
import base64
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

# Mocking the database and current user
class MockUser:
    def __init__(self, id, branch=None):
        self.id = id
        self.branch = branch
        self.attendance_logs = []

class MockBranch:
    def __init__(self, latitude, longitude, radius_meters):
        self.latitude = latitude
        self.longitude = longitude
        self.radius_meters = radius_meters

@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()

def test_create_attendance_success(mocker):
    # 1. Setup mocks
    user_id = uuid4()
    branch = MockBranch(latitude=14.5995, longitude=120.9842, radius_meters=100.0)
    user = MockUser(id=user_id, branch=branch)
    
    # Mocking face_service
    mocker.patch("app.api.v1.endpoints.attendance.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.api.v1.endpoints.attendance.face_service.get_face_encodings", return_value=[np.random.rand(128)])
    mocker.patch("app.api.v1.endpoints.attendance.face_service.compare_faces", return_value=(True, 0.1))
    
    # Mocking DB query for FaceEncoding
    mock_face_encoding = mocker.Mock()
    mock_face_encoding.encoding = DataEncryption.encrypt(np.random.rand(128).astype(np.float64).tobytes())
    
    def mock_refresh(obj):
        obj.id = uuid4()
        obj.timestamp = datetime.now()

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_face_encoding]
    mock_db.refresh.side_effect = mock_refresh
    
    # Override dependencies
    app.dependency_overrides[deps.get_current_user] = lambda: user
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    # 2. Call endpoint
    data = {
        "type": "CLOCK_IN",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "snapshot_base64": "some_base64"
    }
    response = client.post("/api/v1/attendance/", json=data)
    
    # 3. Verify
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["location_verified"] is True
    assert res_data["type"] == "CLOCK_IN"
    
    # Cleanup
    app.dependency_overrides = {}

def test_create_attendance_wrong_location(mocker):
    # 1. Setup mocks
    user_id = uuid4()
    branch = MockBranch(latitude=14.5995, longitude=120.9842, radius_meters=100.0)
    user = MockUser(id=user_id, branch=branch)
    
    mocker.patch("app.api.v1.endpoints.attendance.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.api.v1.endpoints.attendance.face_service.get_face_encodings", return_value=[np.random.rand(128)])
    mocker.patch("app.api.v1.endpoints.attendance.face_service.compare_faces", return_value=(True, 0.1))
    
    mock_face_encoding = mocker.Mock()
    mock_face_encoding.encoding = DataEncryption.encrypt(np.random.rand(128).astype(np.float64).tobytes())
    
    def mock_refresh(obj):
        obj.id = uuid4()
        obj.timestamp = datetime.now()

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_face_encoding]
    mock_db.refresh.side_effect = mock_refresh
    
    app.dependency_overrides[deps.get_current_user] = lambda: user
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    # 2. Call endpoint with far away coordinates (e.g., North Pole)
    data = {
        "type": "CLOCK_IN",
        "latitude": 90.0,
        "longitude": 0.0,
        "snapshot_base64": "some_base64"
    }
    response = client.post("/api/v1/attendance/", json=data)
    
    # 3. Verify
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["location_verified"] is False
    
    app.dependency_overrides = {}

def test_create_attendance_no_face_detected(mocker):
    user = MockUser(id=uuid4())
    mocker.patch("app.api.v1.endpoints.attendance.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.api.v1.endpoints.attendance.face_service.get_face_encodings", return_value=[])
    
    app.dependency_overrides[deps.get_current_user] = lambda: user
    app.dependency_overrides[deps.get_db] = lambda: mocker.Mock()
    
    data = {"type": "CLOCK_IN", "snapshot_base64": "some_base64"}
    response = client.post("/api/v1/attendance/", json=data)
    assert response.status_code == 400
    assert "No face detected" in response.json()["detail"]
    app.dependency_overrides = {}

def test_read_attendance_history(mocker):
    user_id = uuid4()
    log = models.AttendanceLog(id=uuid4(), user_id=user_id, type=models.LogType.CLOCK_IN, timestamp=datetime.now())
    user = MockUser(id=user_id)
    user.attendance_logs = [log]
    
    app.dependency_overrides[deps.get_current_user] = lambda: user
    app.dependency_overrides[deps.get_db] = lambda: mocker.Mock()
    
    response = client.get("/api/v1/attendance/history")
    assert response.status_code == 200
    assert len(response.json()) == 1
    app.dependency_overrides = {}
