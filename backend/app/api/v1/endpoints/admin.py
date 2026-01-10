from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.api import deps
from app.services.email_service import email_service

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

# Branch Endpoints
@router.get("/branches", response_model=List[schemas.Branch])
def read_branches(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    return db.query(models.Branch).all()

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
    Includes branch assignment and email notification.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.status = status_in.status
    
    # Update optional fields if provided
    if status_in.full_name:
        user.full_name = status_in.full_name
    if status_in.employee_id:
        user.employee_id = status_in.employee_id
    
    # Handle branch assignment on approval
    if status_in.status == models.UserStatus.APPROVED:
        if not status_in.branch_id:
            raise HTTPException(status_code=400, detail="Branch assignment is required for approval.")
        
        branch = db.query(models.Branch).filter(models.Branch.id == status_in.branch_id).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found.")
        
        user.branch_id = branch.id
        email_service.send_approval_email(user.email, user.full_name, branch.name)
    
    # Handle rejection reason
    elif status_in.status == models.UserStatus.REJECTED:
        if not status_in.rejection_reason:
            raise HTTPException(status_code=400, detail="Rejection reason is required.")
        
        user.rejection_reason = status_in.rejection_reason
        email_service.send_rejection_email(user.email, user.full_name, user.rejection_reason)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Attendance Endpoints
@router.get("/attendance", response_model=List[schemas.Attendance])
def read_attendance_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    attendance_logs = db.query(models.AttendanceLog).options(joinedload(models.AttendanceLog.user)).offset(skip).limit(limit).all()
    # Manually populate full_name from the loaded user relationship
    for log in attendance_logs:
        log.full_name = log.user.full_name if log.user else None
    return attendance_logs
