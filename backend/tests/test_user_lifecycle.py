import pytest
import enum
from uuid import uuid4
from app.models.models import User, UserRole

def test_user_status_model_exists():
    """Test that User model has a status field and UserStatus enum exists."""
    from app.models.models import UserStatus
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
    from app.schemas import UserCreate, UserStatus
    
    user_in = UserCreate(
        email="new@example.com",
        full_name="New User",
        employee_id="EMP100",
        password="password123"
    )
    assert user_in.status == UserStatus.PENDING

def test_user_schema_status():
    """Test that User schema includes the status field."""
    from app.schemas import User, UserStatus
    
    user_data = {
        "id": uuid4(),
        "email": "test@example.com",
        "full_name": "Test User",
        "employee_id": "EMP999",
        "role": UserRole.EMPLOYEE,
        "status": UserStatus.APPROVED,
        "created_at": "2026-01-08T10:00:00"
    }
    
    user_schema = User(**user_data)
    assert user_schema.status == UserStatus.APPROVED
