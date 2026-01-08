from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
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
    branch_id: Optional[int] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    employee_id: str
    full_name: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime

# Department schemas
class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

# Branch schemas
class BranchBase(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_meters: float = 100.0

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

# Schedule schemas
class ScheduleBase(BaseModel):
    name: str
    start_time: str
    end_time: str
    grace_period_mins: int = 15

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

# Face Enrollment
class FaceEnroll(BaseModel):
    image_base64: str

# Attendance schemas
from .attendance import AttendanceBase, AttendanceCreate, Attendance

