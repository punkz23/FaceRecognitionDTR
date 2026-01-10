from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.api import deps
from app.models.models import UserRole, UserStatus
import pytest
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_approve_user_with_branch(mocker):
    """Test approving a user and assigning a branch."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    mock_user.status = UserStatus.PENDING
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.employee_id = "EMP001"
    mock_user.role = UserRole.EMPLOYEE
    mock_user.is_active = True
    mock_user.department_id = None
    mock_user.branch_id = None
    mock_user.rejection_reason = None
    mock_user.created_at = datetime.now()

    mock_branch = mocker.Mock()
    mock_branch.id = 5
    mock_branch.name = "Main Branch"

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_user, mock_branch]

    mock_email = mocker.patch("app.api.v1.endpoints.admin.email_service")

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "status": UserStatus.APPROVED,
        "branch_id": 5
    }

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{mock_user.id}/status", json=data)
        assert response.status_code == 200
        assert mock_user.status == UserStatus.APPROVED
        assert mock_user.branch_id == 5
        assert mock_email.send_approval_email.called
        mock_email.send_approval_email.assert_called_with("test@example.com", "Test User", "Main Branch")
    finally:
        app.dependency_overrides.clear()

def test_reject_user_with_reason(mocker):
    """Test rejecting a user with a reason."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_user = mocker.Mock()
    mock_user.id = uuid4()
    mock_user.status = UserStatus.PENDING
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.employee_id = "EMP001"
    mock_user.role = UserRole.EMPLOYEE
    mock_user.is_active = True
    mock_user.department_id = None
    mock_user.branch_id = None
    mock_user.rejection_reason = None
    mock_user.created_at = datetime.now()

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    mock_email = mocker.patch("app.api.v1.endpoints.admin.email_service")

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "status": UserStatus.REJECTED,
        "rejection_reason": "Face not clear"
    }

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{mock_user.id}/status", json=data)
        assert response.status_code == 200
        assert mock_user.status == UserStatus.REJECTED
        assert mock_user.rejection_reason == "Face not clear"
        assert mock_email.send_rejection_email.called
        mock_email.send_rejection_email.assert_called_with("test@example.com", "Test User", "Face not clear")
    finally:
        app.dependency_overrides.clear()

def test_update_user_status_not_found(mocker):
    """Test updating status of non-existent user."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{uuid4()}/status", json={"status": "APPROVED", "branch_id": 1})
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()

def test_approve_user_missing_branch_id(mocker):
    """Test approval fails if branch_id is missing."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_user = mocker.Mock()
    mock_user.id = uuid4()

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{mock_user.id}/status", json={"status": "APPROVED"})
        assert response.status_code == 400
        assert "Branch assignment is required" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_approve_user_branch_not_found(mocker):
    """Test approval fails if assigned branch does not exist."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_user = mocker.Mock()
    mock_user.id = uuid4()

    mock_db = mocker.Mock()
    # First call returns user, second call returns None for branch
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_user, None]

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{mock_user.id}/status", json={"status": "APPROVED", "branch_id": 999})
        assert response.status_code == 404
        assert "Branch not found" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_reject_user_missing_reason(mocker):
    """Test rejection fails if rejection_reason is missing."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_user = mocker.Mock()
    mock_user.id = uuid4()

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.patch(f"{settings.API_V1_STR}/admin/users/{mock_user.id}/status", json={"status": "REJECTED"})
        assert response.status_code == 400
        assert "Rejection reason is required" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()