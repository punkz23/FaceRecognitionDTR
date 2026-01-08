from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from app.models.models import LogType

class AttendanceBase(BaseModel):
    type: LogType

class AttendanceCreate(AttendanceBase):
    snapshot_base64: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Attendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    timestamp: datetime
    confidence_score: Optional[float]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_verified: Optional[bool] = None
