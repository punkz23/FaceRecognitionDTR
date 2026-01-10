from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services.face_service import face_service
from app.core.encryption import DataEncryption

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif user.status == models.UserStatus.REJECTED:
        reason = user.rejection_reason or "No reason provided."
        raise HTTPException(status_code=400, detail=f"Account rejected: {reason}")
    elif user.status != models.UserStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Account is not approved yet")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserRegister,
) -> Any:
    """
    Register a new user with face enrollment. Status will be PENDING.
    """
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Validate face data
    img = face_service.decode_image(user_in.image_base64)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    encodings = face_service.get_face_encodings(img)
    if not encodings:
        raise HTTPException(status_code=400, detail="No face detected in the image")
    
    if len(encodings) > 1:
        raise HTTPException(status_code=400, detail="Multiple faces detected. Please ensure only one person is in the frame.")

    # Create User in PENDING status
    db_obj = models.User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        employee_id=user_in.employee_id,
        role=models.UserRole.EMPLOYEE,
        status=models.UserStatus.PENDING,
    )
    db.add(db_obj)
    db.flush() # To get the ID

    # Encrypt and save face encoding
    encoding_bytes = encodings[0].tobytes()
    encrypted_encoding = DataEncryption.encrypt(encoding_bytes)

    db_face = models.FaceEncoding(
        user_id=db_obj.id,
        encoding=encrypted_encoding
    )
    db.add(db_face)
    db.commit()
    db.refresh(db_obj)
    return db_obj
