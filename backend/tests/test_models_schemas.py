import pytest
from uuid import uuid4
from app.models.models import AttendanceLog, LogType
# We will need to define this file and class
# from app.schemas.attendance import AttendanceCreate

def test_branch_model_structure():
    """Test that Branch model has required fields for geofencing."""
    from app.models.models import Branch
    branch = Branch(
        name="Main Branch",
        latitude=14.5995,
        longitude=120.9842,
        radius_meters=100.0
    )
    assert branch.name == "Main Branch"
    assert branch.latitude == 14.5995
    assert branch.longitude == 120.9842
    assert branch.radius_meters == 100.0

def test_user_branch_relationship():
    """Test that User can be associated with a Branch."""
    from app.models.models import User, Branch
    branch = Branch(name="Test Branch", latitude=0, longitude=0)
    user = User(
        employee_id="EMP001",
        full_name="John Doe",
        email="john@example.com",
        hashed_password="hash",
        branch=branch
    )
    assert user.branch == branch

def test_attendance_log_model_structure():
    """Test that AttendanceLog has the required fields including new location fields."""
    user_id = uuid4()
    log = AttendanceLog(
        user_id=user_id,
        type=LogType.CLOCK_IN,
        confidence_score=0.95,
        snapshot_path="/tmp/img.jpg",
        latitude=14.5995,
        longitude=120.9842,
        location_verified=True
    )
    
    assert getattr(log, 'latitude', None) == 14.5995
    assert getattr(log, 'longitude', None) == 120.9842
    assert getattr(log, 'location_verified', None) is True

def test_attendance_schema_exists():
    """Test that the attendance schema module exists and can be imported."""
    try:
        from app.schemas import attendance
        assert hasattr(attendance, "AttendanceCreate")
    except ImportError:
        pytest.fail("Could not import app.schemas.attendance")

def test_attendance_schema_validation():
    """Test Pydantic schema for Attendance creation."""
    try:
        from app.schemas.attendance import AttendanceCreate
        
        data = {
            "type": "CLOCK_IN",
            "latitude": 14.5995,
            "longitude": 120.9842,
            "snapshot_base64": "base64_string"
        }
        
        schema = AttendanceCreate(**data)
        assert schema.latitude == 14.5995
        assert schema.longitude == 120.9842
    except ImportError:
        pytest.fail("Could not import app.schemas.attendance")

def test_branch_schema_validation():
    """Test Pydantic schema for Branch creation."""
    from app.schemas import BranchCreate
    data = {
        "name": "North Branch",
        "latitude": 15.0,
        "longitude": 121.0,
        "radius_meters": 200.0
    }
    schema = BranchCreate(**data)
    assert schema.name == "North Branch"
    assert schema.latitude == 15.0
    assert schema.radius_meters == 200.0
