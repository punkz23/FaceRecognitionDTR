from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.api import deps
from app.models.models import UserRole
import pytest
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_get_all_attendance_logs_admin(mocker):
    """Test that an admin can retrieve all attendance logs."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    # Mock AttendanceLog objects
    mock_log1 = mocker.Mock()
    mock_log1.id = uuid4()
    mock_log1.type = "CLOCK_IN"
    mock_log1.user_id = uuid4()
    mock_log1.timestamp = datetime.now()
    mock_log1.confidence_score = 0.95
    mock_log1.latitude = 14.5
    mock_log1.longitude = 121.0
    mock_log1.location_verified = True
    mock_log1.user.full_name = "User 1" # Added
    
    mock_log2 = mocker.Mock()
    mock_log2.id = uuid4()
    mock_log2.type = "CLOCK_OUT"
    mock_log2.user_id = uuid4()
    mock_log2.timestamp = datetime.now()
    mock_log2.confidence_score = 0.98
    mock_log2.latitude = 14.5
    mock_log2.longitude = 121.0
    mock_log2.location_verified = True
    mock_log2.user.full_name = "User 2" # Added

    mock_db = mocker.Mock()
    
    mock_query_result = mocker.Mock()
    mock_query_result.options.return_value = mock_query_result
    mock_query_result.offset.return_value = mock_query_result
    mock_query_result.limit.return_value = mock_query_result
    mock_query_result.all.return_value = [mock_log1, mock_log2]
    
    mock_db.query.return_value = mock_query_result

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.get(f"{settings.API_V1_STR}/admin/attendance")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["type"] == "CLOCK_IN"
        assert data[1]["type"] == "CLOCK_OUT"
    finally:
        app.dependency_overrides.clear()
