import pytest
from datetime import datetime, timedelta
from app.services.payroll_service import calculate_work_hours
from app.models.models import AttendanceLog, LogType
import uuid

def test_calculate_work_hours_simple():
    user_id = uuid.uuid4()
    logs = [
        AttendanceLog(
            id=uuid.uuid4(),
            user_id=user_id,
            type=LogType.CLOCK_IN,
            timestamp=datetime(2026, 1, 9, 8, 0, 0)
        ),
        AttendanceLog(
            id=uuid.uuid4(),
            user_id=user_id,
            type=LogType.CLOCK_OUT,
            timestamp=datetime(2026, 1, 9, 17, 0, 0)
        )
    ]
    
    total_hours = calculate_work_hours(logs)
    assert total_hours == 9.0

def test_calculate_work_hours_multiple_days():
    user_id = uuid.uuid4()
    logs = [
        # Day 1: 9 hours
        AttendanceLog(type=LogType.CLOCK_IN, timestamp=datetime(2026, 1, 8, 8, 0), user_id=user_id),
        AttendanceLog(type=LogType.CLOCK_OUT, timestamp=datetime(2026, 1, 8, 17, 0), user_id=user_id),
        # Day 2: 8 hours
        AttendanceLog(type=LogType.CLOCK_IN, timestamp=datetime(2026, 1, 9, 9, 0), user_id=user_id),
        AttendanceLog(type=LogType.CLOCK_OUT, timestamp=datetime(2026, 1, 9, 17, 0), user_id=user_id),
    ]
    
    total_hours = calculate_work_hours(logs)
    assert total_hours == 17.0

def test_unmatched_logs():
    user_id = uuid.uuid4()
    logs = [
        AttendanceLog(type=LogType.CLOCK_IN, timestamp=datetime(2026, 1, 8, 8, 0), user_id=user_id),
        # Missing CLOCK_OUT
        AttendanceLog(type=LogType.CLOCK_IN, timestamp=datetime(2026, 1, 9, 8, 0), user_id=user_id),
        AttendanceLog(type=LogType.CLOCK_OUT, timestamp=datetime(2026, 1, 9, 17, 0), user_id=user_id),
    ]
    
    # Only the matched pair should count (9 hours)
    total_hours = calculate_work_hours(logs)
    assert total_hours == 9.0
