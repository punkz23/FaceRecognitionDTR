from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve users.
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new user.
    """
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    db_obj = models.User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        employee_id=user_in.employee_id,
        role=user_in.role,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

from app.services.face_service import face_service
import numpy as np

from app.core.encryption import DataEncryption

@router.post("/{user_id}/face-enroll", response_model=dict)
def enroll_face(
    user_id: str,
    enroll_data: schemas.FaceEnroll,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
):
    """
    Enroll a face for a user.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Decode image
    img = face_service.decode_image(enroll_data.image_base64)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    # Get encodings
    encodings = face_service.get_face_encodings(img)
    if not encodings:
        raise HTTPException(status_code=400, detail="No face detected in the image")
    
    if len(encodings) > 1:
        raise HTTPException(status_code=400, detail="Multiple faces detected. Please ensure only one person is in the frame.")

    # Serialize encoding to bytes and Encrypt
    encoding_bytes = encodings[0].tobytes()
    encrypted_encoding = DataEncryption.encrypt(encoding_bytes)

    # Save to DB
    db_face = models.FaceEncoding(
        user_id=user.id,
        encoding=encrypted_encoding
    )
    db.add(db_face)
    db.commit()
    
    return {"message": "Face enrolled successfully"}
