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
    # 1. Decode image from base64
    img = face_service.decode_image(attendance_in.snapshot_base64)
    if img is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not decode image"
        )

    # 2. Get face encodings
    live_encodings = face_service.get_face_encodings(img)
    if not live_encodings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face detected in image"
        )
    live_encoding = live_encodings[0]

    # 3. Biometric Verification
    stored_faces = db.query(models.FaceEncoding).filter(models.FaceEncoding.user_id == current_user.id).all()
    if not stored_faces:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no enrolled face data"
        )

    match_found = False
    best_score = 1.0 # Lower is better in face_recognition distance
    
    for face_record in stored_faces:
        try:
            decrypted_bytes = DataEncryption.decrypt(face_record.encoding)
            stored_encoding = np.frombuffer(decrypted_bytes, dtype=np.float64)
            
            is_match, distance = face_service.compare_faces(stored_encoding, live_encoding)
            if is_match:
                match_found = True
                if distance < best_score:
                    best_score = distance
        except Exception:
            continue

    if not match_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face verification failed"
        )

    # 4. Location Verification (Geofencing)
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