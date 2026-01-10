from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.api import deps
from app.models.models import UserRole, UserStatus, LogType, AttendanceLog
import pytest
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_create_attendance_location_success(mocker):
    """Test attendance creation with valid location."""
    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    mock_user.status = UserStatus.APPROVED
    
    mock_branch = mocker.Mock()
    mock_branch.latitude = 14.5995
    mock_branch.longitude = 120.9842
    mock_branch.radius_meters = 100.0
    mock_branch.name = "Main Branch"
    
    mock_user.branch = mock_branch

    # Mock face data
    mock_face = mocker.Mock()
    mock_face.encoding = b"fake_encoding"
    
    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_face]

    # Mock face service
    mock_face_service = mocker.patch("app.api.v1.endpoints.attendance.face_service")
    mock_face_service.verify_against_encrypted_storage.return_value = (True, 0.1)

    def mock_refresh(obj):
        obj.id = uuid4()
        obj.timestamp = datetime.now()
    
    mock_db.refresh.side_effect = mock_refresh

    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "type": LogType.CLOCK_IN,
        "snapshot_base64": "fake_base64",
        "latitude": 14.59955, # Approx 5 meters away
        "longitude": 120.98425
    }

    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 200
        assert response.json()["location_verified"] is True
    finally:
        app.dependency_overrides.clear()

def test_create_attendance_location_forbidden(mocker):
    """Test attendance creation rejected if outside geofence."""
    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    mock_user.status = UserStatus.APPROVED
    
    mock_branch = mocker.Mock()
    mock_branch.latitude = 14.5995
    mock_branch.longitude = 120.9842
    mock_branch.radius_meters = 100.0
    mock_branch.name = "Main Branch"
    
    mock_user.branch = mock_branch

    # Mock face data
    mock_face = mocker.Mock()
    mock_face.encoding = b"fake_encoding"
    
    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_face]

    # Mock face service
    mock_face_service = mocker.patch("app.api.v1.endpoints.attendance.face_service")
    mock_face_service.verify_against_encrypted_storage.return_value = (True, 0.1)

    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "type": LogType.CLOCK_IN,
        "snapshot_base64": "fake_base64",
        "latitude": 14.6760, # Quezon City
        "longitude": 121.0437
    }

    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 403
        assert "outside the allowed area" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_create_attendance_no_branch_assigned(mocker):
    """Test attendance creation fails if no branch is assigned."""
    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    mock_user.branch = None # No branch assigned

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mocker.Mock()]

    mocker.patch("app.api.v1.endpoints.attendance.face_service").verify_against_encrypted_storage.return_value = (True, 0.1)

    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "type": LogType.CLOCK_IN,
        "snapshot_base64": "fake_base64",
        "latitude": 14.5995,
        "longitude": 120.9842
    }

    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 403
        assert "no branch assigned" in response.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()

def test_create_attendance_branch_no_geofence(mocker):
    """Test attendance creation rejected if branch has no coordinates."""
    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    
    mock_branch = mocker.Mock()
    mock_branch.latitude = None
    mock_branch.longitude = None
    mock_branch.name = "No Geofence Branch"
    
    mock_user.branch = mock_branch

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mocker.Mock()]

    mocker.patch("app.api.v1.endpoints.attendance.face_service").verify_against_encrypted_storage.return_value = (True, 0.1)

    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "type": LogType.CLOCK_IN,
        "snapshot_base64": "fake_base64",
        "latitude": 14.5995,
        "longitude": 120.9842
    }

    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 403
        assert "no geofence configured" in response.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()

def test_create_attendance_missing_coords(mocker):
    """Test attendance creation rejected if coordinates are missing."""
    mock_user = mocker.Mock()
    mock_user.id = uuid4()

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mocker.Mock()]

    mocker.patch("app.api.v1.endpoints.attendance.face_service").verify_against_encrypted_storage.return_value = (True, 0.1)

    app.dependency_overrides[deps.get_current_user] = lambda: mock_user
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "type": LogType.CLOCK_IN,
        "snapshot_base64": "fake_base64",
        "latitude": None,
        "longitude": None
    }

    try:
        response = client.post(f"{settings.API_V1_STR}/attendance/", json=data)
        assert response.status_code == 400
        assert "location coordinates are required" in response.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()