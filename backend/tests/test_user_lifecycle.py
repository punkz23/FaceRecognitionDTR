import pytest
import enum
from uuid import uuid4, UUID
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.models.models import User, UserRole, UserStatus
from app.api import deps

client = TestClient(app)

def test_user_status_model_exists():
    """Test that User model has a status field and UserStatus enum exists."""
    assert issubclass(UserStatus, str)
    assert issubclass(UserStatus, enum.Enum)
    assert "PENDING" in UserStatus.__members__
    assert "APPROVED" in UserStatus.__members__
    assert "REJECTED" in UserStatus.__members__

    user = User(
        employee_id="EMP002",
        full_name="Jane Doe",
        email="jane@example.com",
        hashed_password="hash",
        status=UserStatus.PENDING
    )
    assert user.status == UserStatus.PENDING

def test_user_schema_status_default():
    """Test that UserCreate schema has a default status of PENDING."""
    from app.schemas import UserCreate
    
    user_in = UserCreate(
        email="new@example.com",
        full_name="New User",
        employee_id="EMP100",
        password="password123"
    )
    assert user_in.status == UserStatus.PENDING

def test_user_schema_status():
    """Test that User schema includes the status field."""
    from app.schemas import User as UserSchema
    
    user_data = {
        "id": uuid4(),
        "email": "test@example.com",
        "full_name": "Test User",
        "employee_id": "EMP999",
        "role": UserRole.EMPLOYEE,
        "status": UserStatus.APPROVED,
        "created_at": datetime.now()
    }
    
    user_schema = UserSchema(**user_data)
    assert user_schema.status == UserStatus.APPROVED

def test_register_user_success(mocker):
    """Test successful user registration with face data."""
    # Mock face service and DB
    mock_face_service = mocker.patch("app.api.v1.endpoints.auth.face_service")
    mock_face_service.decode_image.return_value = "fake_img"
    
    mock_encoding = mocker.Mock()
    mock_encoding.tobytes.return_value = b"fake_bytes"
    mock_face_service.get_face_encodings.return_value = [mock_encoding]
    
    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None # No existing user
    
    def mock_add(obj):
        obj.id = uuid4()
        obj.created_at = datetime.now()
    
    mock_db.add.side_effect = mock_add
    
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    data = {
        "email": "new_reg@example.com",
        "password": "password123",
        "full_name": "New Reg User",
        "employee_id": "EMP555",
        "image_base64": "fake_base64"
    }
    
    try:
        response = client.post(f"{settings.API_V1_STR}/auth/register", json=data)
        assert response.status_code == 200
        assert response.json()["email"] == "new_reg@example.com"
        assert response.json()["status"] == "PENDING"
        assert mock_db.add.called
        assert mock_db.commit.called
    finally:
        app.dependency_overrides.clear()

def test_login_pending_user_fails(mocker):
    """Test that a PENDING user cannot log in."""
    mock_user = mocker.Mock()
    mock_user.email = "pending@example.com"
    mock_user.hashed_password = "hashed_password"
    mock_user.is_active = True
    mock_user.status = UserStatus.PENDING
    
    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    mocker.patch("app.core.security.verify_password", return_value=True)
    
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    login_data = {
        "username": "pending@example.com",
        "password": "password123"
    }
    
    try:
        response = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
        assert response.status_code == 400
        assert "not approved" in response.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()

def test_admin_approve_user_success(mocker):
    """Test that an admin can approve a user."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN
    
    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    mock_user.status = UserStatus.PENDING
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.employee_id = "EMP999"
    mock_user.role = UserRole.EMPLOYEE
    mock_user.is_active = True
    mock_user.department_id = None
    mock_user.branch_id = None
    mock_user.rejection_reason = None
    mock_user.created_at = datetime.now()    
    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db
    
    user_id = str(mock_user.id)
    data = {"status": "APPROVED", "branch_id": 1}
    
    mock_branch = mocker.Mock()
    mock_branch.id = 1
    mock_branch.name = "Test Branch"
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_user, mock_branch]
    
    # Mock email service to avoid errors
    mocker.patch("app.api.v1.endpoints.admin.email_service")

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{user_id}/status", json=data)
        assert response.status_code == 200
        assert response.json()["status"] == "APPROVED"
        assert mock_user.status == UserStatus.APPROVED
        assert mock_db.commit.called
    finally:
        app.dependency_overrides.clear()

def test_admin_approve_user_unauthorized(mocker):
    """Test that a non-admin cannot approve a user."""
    user_id = str(uuid4())
    data = {"status": "APPROVED"}
    
    response = client.patch(f"{settings.API_V1_STR}/admin/users/{user_id}/status", json=data)
    assert response.status_code == 401 # Unauthorized