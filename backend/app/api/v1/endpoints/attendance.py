from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services.face_service import face_service
from app.core.encryption import DataEncryption
import numpy as np
import math

router = APIRouter()

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # radius of the earth in meters
    R = 6371000
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@router.post("/", response_model=schemas.Attendance)
def create_attendance(
    *,
    db: Session = Depends(deps.get_db),
    attendance_in: schemas.AttendanceCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new attendance log with face and location verification.
    """
    # 1. Fetch stored face data
    stored_faces = db.query(models.FaceEncoding).filter(models.FaceEncoding.user_id == current_user.id).all()
    if not stored_faces:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no enrolled face data"
        )
    stored_encodings = [f.encoding for f in stored_faces]

    # 2. Biometric Verification
    try:
        is_match, distance = face_service.verify_against_encrypted_storage(
            attendance_in.snapshot_base64, 
            stored_encodings
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not is_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face verification failed"
        )
    
    best_score = distance

    # 3. Location Verification (Geofencing)
    location_verified = False
    if attendance_in.latitude is not None and attendance_in.longitude is not None:
        if current_user.branch and current_user.branch.latitude and current_user.branch.longitude:
            dist = calculate_distance(
                attendance_in.latitude,
                attendance_in.longitude,
                current_user.branch.latitude,
                current_user.branch.longitude
            )
            if dist <= current_user.branch.radius_meters:
                location_verified = True
    
    # 5. Create Attendance Log
    db_obj = models.AttendanceLog(
        user_id=current_user.id,
        type=attendance_in.type,
        confidence_score=float(1.0 - best_score),
        snapshot_path=None, # Placeholder
        latitude=attendance_in.latitude,
        longitude=attendance_in.longitude,
        location_verified=location_verified
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj

@router.get("/history", response_model=List[schemas.Attendance])
def read_attendance_history(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve attendance history for the current user.
    """
    return current_user.attendance_logs