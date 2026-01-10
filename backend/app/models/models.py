from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.base_class import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"

class UserStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class LogType(str, enum.Enum):
    CLOCK_IN = "CLOCK_IN"
    CLOCK_OUT = "CLOCK_OUT"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)
    rejection_reason = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    department = relationship("Department", back_populates="users")
    branch = relationship("Branch", back_populates="users")
    attendance_logs = relationship("AttendanceLog", back_populates="user")
    face_encodings = relationship("FaceEncoding", back_populates="user")

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    users = relationship("User", back_populates="department")

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    radius_meters = Column(Float, default=100.0)
    
    users = relationship("User", back_populates="branch")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_time = Column(String, nullable=False) # e.g. "08:00"
    end_time = Column(String, nullable=False)   # e.g. "17:00"
    grace_period_mins = Column(Integer, default=15)

class FaceEncoding(Base):
    __tablename__ = "face_encodings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    encoding = Column(LargeBinary, nullable=False)  # Storing numpy array as bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="face_encodings")

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    type = Column(Enum(LogType), nullable=False)
    confidence_score = Column(Float, nullable=True)
    snapshot_path = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="attendance_logs")
