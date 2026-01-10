from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.api import deps
from app.models.models import UserRole, Branch
from app.schemas import BranchCreate, Branch as BranchSchema
import pytest

client = TestClient(app)

def test_create_branch_success(mocker):
    """Test creating a new branch."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_db = mocker.Mock()
    # Mock branch doesn't exist
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Mock DB add/commit
    def mock_add(obj):
        obj.id = 1
    mock_db.add.side_effect = mock_add

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "name": "New Branch",
        "address": "456 Test Ave",
        "latitude": 10.5,
        "longitude": 20.5,
        "radius_meters": 150.0
    }

    try:
        response = client.post(f"{settings.API_V1_STR}/branches/", json=data)
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "New Branch"
        assert content["address"] == "456 Test Ave"
        assert content["radius_meters"] == 150.0
        assert mock_db.add.called
        assert mock_db.commit.called
    finally:
        app.dependency_overrides.clear()

def test_read_branches_success(mocker):
    """Test listing branches."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_branch = mocker.Mock()
    mock_branch.id = 1
    mock_branch.name = "Branch 1"
    mock_branch.address = "Address 1"
    mock_branch.latitude = 0.0
    mock_branch.longitude = 0.0
    mock_branch.radius_meters = 100.0

    mock_db = mocker.Mock()
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_branch]

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.get(f"{settings.API_V1_STR}/branches/")
        assert response.status_code == 200
        content = response.json()
        assert isinstance(content, list)
        assert len(content) == 1
        assert content[0]["name"] == "Branch 1"
    finally:
        app.dependency_overrides.clear()

def test_update_branch_success(mocker):
    """Test updating a branch."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_branch = mocker.Mock()
    mock_branch.id = 1
    mock_branch.name = "Old Name"
    mock_branch.address = "Old Address"
    mock_branch.latitude = 10.0
    mock_branch.longitude = 20.0
    mock_branch.radius_meters = 100.0

    mock_db = mocker.Mock()
    # Return mock_branch when queried by ID
    mock_db.query.return_value.filter.return_value.first.return_value = mock_branch

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {
        "name": "Updated Name",
        "address": "Updated Address"
    }

    try:
        response = client.patch(f"{settings.API_V1_STR}/branches/1", json=data)
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "Updated Name"
        assert content["address"] == "Updated Address"
        assert mock_branch.name == "Updated Name"
        assert mock_db.commit.called
    finally:
        app.dependency_overrides.clear()

def test_delete_branch_success(mocker):
    """Test deleting a branch."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_branch = mocker.Mock()
    mock_branch.id = 1
    mock_branch.name = "Branch to Delete"
    mock_branch.address = "Address"
    mock_branch.latitude = 10.0
    mock_branch.longitude = 20.0
    mock_branch.radius_meters = 100.0

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_branch

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.delete(f"{settings.API_V1_STR}/branches/1")
        assert response.status_code == 200
        assert mock_db.delete.called
        assert mock_db.commit.called
    finally:
        app.dependency_overrides.clear()

def test_create_branch_already_exists(mocker):
    """Test creating a branch that already exists."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mocker.Mock() # Branch exists

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    data = {"name": "Existing Branch"}

    try:
        response = client.post(f"{settings.API_V1_STR}/branches/", json=data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_update_branch_not_found(mocker):
    """Test updating a non-existent branch."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.patch(f"{settings.API_V1_STR}/branches/999", json={"name": "New"})
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()

def test_delete_branch_not_found(mocker):
    """Test deleting a non-existent branch."""
    mock_admin = mocker.Mock()
    mock_admin.role = UserRole.ADMIN

    mock_db = mocker.Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    app.dependency_overrides[deps.get_current_active_admin] = lambda: mock_admin
    app.dependency_overrides[deps.get_db] = lambda: mock_db

    try:
        response = client.delete(f"{settings.API_V1_STR}/branches/999")
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()