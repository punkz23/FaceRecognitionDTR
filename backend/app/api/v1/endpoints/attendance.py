from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services.face_service import face_service
from app.core.encryption import DataEncryption
from app.core.location_utils import calculate_distance
import numpy as np

router = APIRouter()

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

    # 3. Location Verification (Geofencing) - Strict Enforcement
    if attendance_in.latitude is None or attendance_in.longitude is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location coordinates are required."
        )

    if not current_user.branch:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no branch assigned. Please contact your administrator."
        )

    if not current_user.branch.latitude or not current_user.branch.longitude:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Branch '{current_user.branch.name}' has no geofence configured."
        )

    dist = calculate_distance(
        attendance_in.latitude,
        attendance_in.longitude,
        current_user.branch.latitude,
        current_user.branch.longitude
    )
    
    if dist > current_user.branch.radius_meters:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are outside the allowed area for your assigned branch ({current_user.branch.name})."
        )
    
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
    
    # Ensure attributes are loaded for response
    _ = db_obj.id
    _ = db_obj.timestamp
    
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