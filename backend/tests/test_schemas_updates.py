
from app.schemas import User, BranchCreate, UserStatusUpdate, UserStatus
import pytest
from pydantic import ValidationError

def test_user_schema_has_rejection_reason():
    """Test that User schema has the rejection_reason field."""
    # We create a dummy User object (mimicking a DB record or dict)
    data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "full_name": "Test User",
        "employee_id": "E123",
        "role": "EMPLOYEE",
        "status": "PENDING",
        "created_at": "2023-01-01T00:00:00",
        "rejection_reason": "Face not clear"
    }
    user = User(**data)
    assert user.rejection_reason == "Face not clear"

def test_branch_schema_has_address():
    """Test that Branch schema has the address field."""
    data = {
        "name": "Main Branch",
        "address": "123 Main St",
        "latitude": 10.0,
        "longitude": 20.0,
        "radius_meters": 100.0
    }
    branch = BranchCreate(**data)
    assert branch.address == "123 Main St"

def test_user_status_update_schema():
    """Test UserStatusUpdate accepts rejection_reason and branch_id."""
    # Test Approval with Branch
    data_approve = {
        "status": UserStatus.APPROVED,
        "branch_id": 5
    }
    update_approve = UserStatusUpdate(**data_approve)
    assert update_approve.status == UserStatus.APPROVED
    assert update_approve.branch_id == 5

    # Test Rejection with Reason
    data_reject = {
        "status": UserStatus.REJECTED,
        "rejection_reason": "Invalid ID"
    }
    update_reject = UserStatusUpdate(**data_reject)
    assert update_reject.status == UserStatus.REJECTED
    assert update_reject.rejection_reason == "Invalid ID"
