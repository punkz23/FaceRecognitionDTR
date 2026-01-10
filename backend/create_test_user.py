import sys
import os
import numpy as np
from sqlalchemy.orm import Session

# Add the current directory to sys.path to ensure 'app' can be imported
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models import User, FaceEncoding, UserStatus, UserRole
from app.core.security import get_password_hash
from app.core.encryption import DataEncryption

def create_test_user():
    db = SessionLocal()
    try:
        # User details for the requested admin user
        email = "iggy@example.com"
        password = "password"
        employee_id = "ADMIN001" # Unique ID for admin
        full_name = "Iggy Admin"
        
        # Check if user already exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"Admin user {email} already exists. Ensuring role is ADMIN and status is APPROVED.")
            user.role = UserRole.ADMIN
            user.status = UserStatus.APPROVED
            db.commit()
            return

        print(f"Creating admin user: {email}")
        
        # Create user
        db_user = User(
            email=email,
            hashed_password=get_password_hash(password),
            employee_id=employee_id,
            full_name=full_name,
            role=UserRole.ADMIN, # Set role to ADMIN
            status=UserStatus.APPROVED,
            is_active=True
        )
        db.add(db_user)
        db.flush()  # Get the ID
        
        # Create fake face encoding (128 floats)
        fake_encoding = np.random.rand(128).astype(np.float64)
        encoding_bytes = fake_encoding.tobytes()
        encrypted_encoding = DataEncryption.encrypt(encoding_bytes)
        
        db_face = FaceEncoding(
            user_id=db_user.id,
            encoding=encrypted_encoding,
            image_path="/static/faces/admin001.jpg" # Placeholder image path
        )
        db.add(db_face)
        
        db.commit()
        print(f"Successfully created admin user: {email} with password: {password}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()