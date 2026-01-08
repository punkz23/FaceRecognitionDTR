from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import pytest

client = TestClient(app)

def test_attendance_endpoint_exists():
    """Test that POST /attendance endpoint exists."""
    response = client.post(f"{settings.API_V1_STR}/attendance/", json={})
    # If the endpoint doesn't exist, FastAPI returns 404.
    # If it exists but requires auth, it returns 401.
    # If it exists but validation fails, it returns 422.
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
