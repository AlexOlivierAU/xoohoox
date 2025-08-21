from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import fermentation_trial as crud
from app.schemas.fermentation_trial import (
    FermentationTrialCreate,
    FermentationTrialUpdate,
    FermentationTrialInDB,
    FermentationTrialList,
    DailyReadingCreate,
    UpscaleEventCreate,
    PathTaken
)

router = APIRouter()

@router.get("/{trial_id}", response_model=FermentationTrialInDB)
def get_trial(
    trial_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific fermentation trial by ID."""
    db_trial = crud.get_trial(db, trial_id)
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return db_trial

@router.get("/batch/{batch_id}", response_model=FermentationTrialList)
def get_batch_trials(
    batch_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all trials for a specific batch."""
    trials = crud.get_trials_by_batch(db, batch_id, skip, limit)
    return {
        "trials": trials,
        "total": len(trials)
    }

@router.post("/", response_model=FermentationTrialInDB)
def create_trial(
    trial: FermentationTrialCreate,
    db: Session = Depends(get_db)
):
    """Create a new fermentation trial."""
    return crud.create_trial(db, trial)

@router.patch("/{trial_id}", response_model=FermentationTrialInDB)
def update_trial(
    trial_id: int,
    trial_update: FermentationTrialUpdate,
    db: Session = Depends(get_db)
):
    """Update a fermentation trial."""
    db_trial = crud.update_trial(db, trial_id, trial_update)
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return db_trial

@router.post("/{trial_id}/readings", response_model=FermentationTrialInDB)
def add_daily_reading(
    trial_id: int,
    reading: DailyReadingCreate,
    db: Session = Depends(get_db)
):
    """Add a daily reading to a trial."""
    db_trial = crud.record_daily_reading(db, trial_id, reading)
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return db_trial

@router.post("/{trial_id}/upscale", response_model=FermentationTrialInDB)
def record_upscale(
    trial_id: int,
    upscale: UpscaleEventCreate,
    db: Session = Depends(get_db)
):
    """Record an upscale event for a trial."""
    db_trial = crud.record_upscale(db, trial_id, upscale)
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return db_trial

@router.post("/{trial_id}/path", response_model=FermentationTrialInDB)
def set_trial_path(
    trial_id: int,
    path: PathTaken,
    db: Session = Depends(get_db)
):
    """Set the path taken for a trial (vinegar, distillation, or archived)."""
    db_trial = crud.set_trial_path(db, trial_id, path)
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return db_trial

@router.post("/{trial_id}/compound-results", response_model=FermentationTrialInDB)
def update_compound_results(
    trial_id: int,
    results: dict,
    db: Session = Depends(get_db)
):
    """Update compound test results for a trial."""
    db_trial = crud.update_compound_results(db, trial_id, results)
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return db_trial 