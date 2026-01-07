from typing import Optional, List
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    employee_id: Optional[str] = None
    role: UserRole = UserRole.EMPLOYEE
    department_id: Optional[int] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    employee_id: str
    full_name: str

class User(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Department schemas
class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

# Schedule schemas
class ScheduleBase(BaseModel):
    name: str
    start_time: str
    end_time: str
    grace_period_mins: int = 15

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    class Config:
        from_attributes = True

# Face Enrollment
class FaceEnroll(BaseModel):
    image_base64: str

# Attendance schemas
class AttendanceBase(BaseModel):
    type: str

class AttendanceCreate(AttendanceBase):
    image_base64: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Attendance(AttendanceBase):
    id: UUID
    user_id: UUID
    timestamp: datetime
    confidence_score: Optional[float]
    
    class Config:
        from_attributes = True
