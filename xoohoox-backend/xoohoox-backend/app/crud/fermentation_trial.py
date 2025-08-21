from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.fermentation_trial import FermentationTrial, PathTaken
from app.schemas.fermentation_trial import (
    FermentationTrialCreate,
    FermentationTrialUpdate,
    DailyReadingCreate,
    UpscaleEventCreate
)

def get_trial(db: Session, trial_id: int) -> Optional[FermentationTrial]:
    return db.query(FermentationTrial).filter(FermentationTrial.id == trial_id).first()

def get_trial_by_trial_id(db: Session, trial_id: str) -> Optional[FermentationTrial]:
    return db.query(FermentationTrial).filter(FermentationTrial.trial_id == trial_id).first()

def get_trials_by_batch(
    db: Session, 
    batch_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[FermentationTrial]:
    return (
        db.query(FermentationTrial)
        .filter(FermentationTrial.batch_id == batch_id)
        .order_by(desc(FermentationTrial.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_trial(
    db: Session, 
    trial: FermentationTrialCreate
) -> FermentationTrial:
    # Generate trial_id based on batch and sequence
    batch_trials = get_trials_by_batch(db, trial.batch_id)
    trial_sequence = len(batch_trials) + 1
    trial_id = f"T-{trial.batch_id:03d}-{trial_sequence:02d}"
    
    db_trial = FermentationTrial(
        trial_id=trial_id,
        **trial.model_dump()
    )
    db.add(db_trial)
    db.commit()
    db.refresh(db_trial)
    return db_trial

def update_trial(
    db: Session,
    trial_id: int,
    trial_update: FermentationTrialUpdate
) -> Optional[FermentationTrial]:
    db_trial = get_trial(db, trial_id)
    if not db_trial:
        return None
    
    update_data = trial_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_trial, field, value)
    
    db.commit()
    db.refresh(db_trial)
    return db_trial

def record_daily_reading(
    db: Session,
    trial_id: int,
    reading: DailyReadingCreate
) -> Optional[FermentationTrial]:
    db_trial = get_trial(db, trial_id)
    if not db_trial:
        return None
    
    db_trial.record_daily_reading(**reading.model_dump())
    db.commit()
    db.refresh(db_trial)
    return db_trial

def record_upscale(
    db: Session,
    trial_id: int,
    upscale: UpscaleEventCreate
) -> Optional[FermentationTrial]:
    db_trial = get_trial(db, trial_id)
    if not db_trial:
        return None
    
    db_trial.record_upscale(**upscale.model_dump())
    db.commit()
    db.refresh(db_trial)
    return db_trial

def set_trial_path(
    db: Session,
    trial_id: int,
    path: PathTaken
) -> Optional[FermentationTrial]:
    db_trial = get_trial(db, trial_id)
    if not db_trial:
        return None
    
    db_trial.set_path(path)
    db.commit()
    db.refresh(db_trial)
    return db_trial

def update_compound_results(
    db: Session,
    trial_id: int,
    results: Dict[str, Any]
) -> Optional[FermentationTrial]:
    db_trial = get_trial(db, trial_id)
    if not db_trial:
        return None
    
    db_trial.compound_results = results
    db.commit()
    db.refresh(db_trial)
    return db_trial 