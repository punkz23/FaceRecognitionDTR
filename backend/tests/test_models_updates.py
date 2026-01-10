
from app.models.models import User, Branch
import pytest

def test_user_model_has_rejection_reason():
    """Test that User model has the rejection_reason field."""
    user = User()
    assert hasattr(user, 'rejection_reason'), "User model missing 'rejection_reason' field"

def test_branch_model_has_address():
    """Test that Branch model has the address field."""
    branch = Branch()
    assert hasattr(branch, 'address'), "Branch model missing 'address' field"
