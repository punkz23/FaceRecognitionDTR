from typing import List
from app.models.models import AttendanceLog, LogType
from datetime import datetime

def calculate_work_hours(logs: List[AttendanceLog]) -> float:
    """
    Calculate total work hours from a list of attendance logs.
    Assumes logs are for a single user and can span multiple days.
    Matches CLOCK_IN with the next available CLOCK_OUT.
    """
    # Sort logs by timestamp
    sorted_logs = sorted(logs, key=lambda x: x.timestamp)
    
    total_seconds = 0.0
    last_in_time = None
    
    for log in sorted_logs:
        if log.type == LogType.CLOCK_IN:
            last_in_time = log.timestamp
        elif log.type == LogType.CLOCK_OUT and last_in_time:
            duration = log.timestamp - last_in_time
            total_seconds += duration.total_seconds()
            last_in_time = None # Reset after matching
            
    return total_seconds / 3600.0
