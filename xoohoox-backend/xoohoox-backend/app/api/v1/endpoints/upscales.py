from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.upscale import UpscaleStatus

router = APIRouter()

@router.get("/{trial_id}/upscales", response_model=List[schemas.UpscaleRunInDB])
def get_trial_upscales(
    trial_id: int,
    db: Session = Depends(deps.get_db),
):
    """Get all upscales for a specific trial"""
    return crud.upscale.get_upscales_by_trial(db, trial_id=trial_id)

@router.post("/{trial_id}/upscales", response_model=schemas.UpscaleRunInDB)
def create_trial_upscale(
    trial_id: int,
    *,
    db: Session = Depends(deps.get_db),
    upscale_in: schemas.UpscaleRunCreate,
):
    """Create a new upscale run for a trial"""
    # Check if there's already an active upscale
    active_upscale = crud.upscale.get_active_upscale_for_trial(db, trial_id=trial_id)
    if active_upscale:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trial already has an active upscale run"
        )
    
    return crud.upscale.create_upscale(db, obj_in=upscale_in)

@router.patch("/upscales/{upscale_id}", response_model=schemas.UpscaleRunInDB)
def update_upscale(
    upscale_id: int,
    *,
    db: Session = Depends(deps.get_db),
    upscale_in: schemas.UpscaleRunUpdate,
):
    """Update upscale run details"""
    db_obj = crud.upscale.get_upscale(db, upscale_id=upscale_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upscale run not found"
        )
    return crud.upscale.update_upscale(db, db_obj=db_obj, obj_in=upscale_in)

@router.post("/upscales/{upscale_id}/complete", response_model=schemas.UpscaleRunInDB)
def complete_upscale(
    upscale_id: int,
    db: Session = Depends(deps.get_db),
):
    """Mark an upscale run as complete"""
    db_obj = crud.upscale.get_upscale(db, upscale_id=upscale_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upscale run not found"
        )
    
    # Validate that required fields are filled
    if not all([db_obj.yield_amount, db_obj.abv_result]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot complete upscale: yield and ABV results required"
        )
    
    update_data = schemas.UpscaleRunUpdate(status=UpscaleStatus.COMPLETE)
    return crud.upscale.update_upscale(db, db_obj=db_obj, obj_in=update_data) 