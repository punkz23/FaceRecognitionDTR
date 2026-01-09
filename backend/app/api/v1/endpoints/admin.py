from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps

router = APIRouter()

# Department Endpoints
@router.get("/departments", response_model=List[schemas.Department])
def read_departments(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    return db.query(models.Department).all()

@router.post("/departments", response_model=schemas.Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    dept_in: schemas.DepartmentCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    db_obj = models.Department(name=dept_in.name)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Schedule Endpoints
@router.get("/schedules", response_model=List[schemas.Schedule])
def read_schedules(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    return db.query(models.Schedule).all()

@router.post("/schedules", response_model=schemas.Schedule)
def create_schedule(
    *,
    db: Session = Depends(deps.get_db),
    sched_in: schemas.ScheduleCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    db_obj = models.Schedule(**sched_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.patch("/users/{user_id}/status", response_model=schemas.User)
def update_user_status(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID,
    status_in: schemas.UserStatusUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update user status (e.g., approve or reject a registration).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.status = status_in.status
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
