from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps

router = APIRouter()

# from app.services.face_service import face_service
# import numpy as np

from app.core.encryption import DataEncryption

@router.post("/clock-in", response_model=schemas.Attendance)
def clock_in(
    *,
    db: Session = Depends(deps.get_db),
    attendance_in: schemas.AttendanceCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Clock in with face recognition.
    """
    # 1. Decode the incoming image
    img = face_service.decode_image(attendance_in.image_base64)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    # 2. Get the encoding of the live face
    live_encodings = face_service.get_face_encodings(img)
    if not live_encodings:
        raise HTTPException(status_code=400, detail="No face detected")
    
    live_encoding = live_encodings[0]

    # 3. Retrieve user's stored embeddings
    stored_faces = db.query(models.FaceEncoding).filter(models.FaceEncoding.user_id == current_user.id).all()
    if not stored_faces:
        raise HTTPException(status_code=400, detail="No enrolled face data found for this user")

    # 4. Compare faces
    match_found = False
    best_score = 1.0 # Lower is better
    
    for face_record in stored_faces:
        # Decrypt and deserialize
        try:
            decrypted_bytes = DataEncryption.decrypt(face_record.encoding)
            stored_encoding = np.frombuffer(decrypted_bytes, dtype=np.float64)
        except Exception:
            continue # Skip corrupted/invalid records

        is_match, distance = face_service.compare_faces(stored_encoding, live_encoding)
        if is_match:
            match_found = True
            if distance < best_score:
                best_score = distance

    if not match_found:
        raise HTTPException(status_code=401, detail="Face verification failed")

    # 5. Log Attendance
    db_obj = models.AttendanceLog(
        user_id=current_user.id,
        type=models.LogType.CLOCK_IN,
        confidence_score=1.0 - best_score, # Convert distance to confidence (approx)
        snapshot_path="s3://bucket/path/to/image.jpg" # Placeholder for image upload
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
