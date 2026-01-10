
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Branch])
def read_branches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve branches.
    """
    branches = db.query(models.Branch).offset(skip).limit(limit).all()
    return branches

@router.post("/", response_model=schemas.Branch)
def create_branch(
    *,
    db: Session = Depends(deps.get_db),
    branch_in: schemas.BranchCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new branch.
    """
    branch = db.query(models.Branch).filter(models.Branch.name == branch_in.name).first()
    if branch:
        raise HTTPException(
            status_code=400,
            detail="The branch with this name already exists.",
        )
    branch = models.Branch(
        name=branch_in.name,
        address=branch_in.address,
        latitude=branch_in.latitude,
        longitude=branch_in.longitude,
        radius_meters=branch_in.radius_meters,
    )
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch

@router.patch("/{branch_id}", response_model=schemas.Branch)
def update_branch(
    *,
    db: Session = Depends(deps.get_db),
    branch_id: int,
    branch_in: schemas.BranchUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update a branch.
    """
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found",
        )
    update_data = branch_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(branch, field, value)
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch

@router.delete("/{branch_id}", response_model=schemas.Branch)
def delete_branch(
    *,
    db: Session = Depends(deps.get_db),
    branch_id: int,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a branch.
    """
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found",
        )
    db.delete(branch)
    db.commit()
    return branch
