
from app.services.email_service import email_service
import pytest

def test_send_approval_email(capsys):
    """Test that approval email prints correct message."""
    email_service.send_approval_email("test@example.com", "Test User", "Main Branch")
    captured = capsys.readouterr()
    assert "SENT APPROVAL EMAIL to test@example.com" in captured.out
    assert "Main Branch" in captured.out

def test_send_rejection_email(capsys):
    """Test that rejection email prints correct message."""
    email_service.send_rejection_email("test@example.com", "Test User", "Face not clear")
    captured = capsys.readouterr()
    assert "SENT REJECTION EMAIL to test@example.com" in captured.out
    assert "Face not clear" in captured.out
