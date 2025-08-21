from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.upscale import UpscaleRun, UpscaleStage
from app.schemas.upscale import UpscaleRunCreate, UpscaleRunUpdate

def generate_upscale_id(trial_id: str, volume: float) -> str:
    """Generate upscale ID in format U-042-03-5L"""
    return f"U-{trial_id}-{int(volume)}L"

def get_upscale(db: Session, upscale_id: int) -> Optional[UpscaleRun]:
    return db.query(UpscaleRun).filter(UpscaleRun.id == upscale_id).first()

def get_upscales_by_trial(db: Session, trial_id: int) -> List[UpscaleRun]:
    return db.query(UpscaleRun).filter(UpscaleRun.trial_id == trial_id).all()

def create_upscale(db: Session, *, obj_in: UpscaleRunCreate) -> UpscaleRun:
    obj_in_data = jsonable_encoder(obj_in)
    upscale_id = generate_upscale_id(str(obj_in.trial_id), obj_in.volume)
    db_obj = UpscaleRun(**obj_in_data, upscale_id=upscale_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_upscale(
    db: Session,
    *,
    db_obj: UpscaleRun,
    obj_in: UpscaleRunUpdate
) -> UpscaleRun:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_upscale(db: Session, *, id: int) -> UpscaleRun:
    obj = db.query(UpscaleRun).get(id)
    db.delete(obj)
    db.commit()
    return obj

def get_active_upscale_for_trial(db: Session, trial_id: int) -> Optional[UpscaleRun]:
    """Get the currently active upscale run for a trial"""
    return db.query(UpscaleRun)\
        .filter(UpscaleRun.trial_id == trial_id)\
        .filter(UpscaleRun.status == "pending")\
        .first() 