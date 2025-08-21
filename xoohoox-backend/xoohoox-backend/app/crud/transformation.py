from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.transformation import (
    TransformationStage,
    JuicingResults,
    FermentationResults
)
from app.schemas.transformation import (
    TransformationStageCreate,
    TransformationStageUpdate,
    JuicingResultsCreate,
    JuicingResultsUpdate,
    FermentationResultsCreate,
    FermentationResultsUpdate
)

# Transformation Stage CRUD operations
def create_transformation_stage(
    db: Session,
    stage: TransformationStageCreate
) -> TransformationStage:
    db_stage = TransformationStage(**stage.model_dump())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def get_transformation_stage(
    db: Session,
    stage_id: int
) -> Optional[TransformationStage]:
    return db.query(TransformationStage).filter(
        TransformationStage.id == stage_id
    ).first()

def get_transformation_stages(
    db: Session,
    batch_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[TransformationStage]:
    query = db.query(TransformationStage)
    if batch_id:
        query = query.filter(TransformationStage.batch_id == batch_id)
    return query.offset(skip).limit(limit).all()

def update_transformation_stage(
    db: Session,
    stage_id: int,
    stage_update: TransformationStageUpdate
) -> Optional[TransformationStage]:
    db_stage = get_transformation_stage(db, stage_id)
    if db_stage:
        update_data = stage_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_stage, field, value)
        db.commit()
        db.refresh(db_stage)
    return db_stage

def delete_transformation_stage(
    db: Session,
    stage_id: int
) -> bool:
    db_stage = get_transformation_stage(db, stage_id)
    if db_stage:
        db.delete(db_stage)
        db.commit()
        return True
    return False

# Juicing Results CRUD operations
def create_juicing_results(
    db: Session,
    results: JuicingResultsCreate
) -> JuicingResults:
    db_results = JuicingResults(**results.model_dump())
    db.add(db_results)
    db.commit()
    db.refresh(db_results)
    return db_results

def get_juicing_results(
    db: Session,
    stage_id: int
) -> Optional[JuicingResults]:
    return db.query(JuicingResults).filter(
        JuicingResults.transformation_stage_id == stage_id
    ).first()

def update_juicing_results(
    db: Session,
    stage_id: int,
    results_update: JuicingResultsUpdate
) -> Optional[JuicingResults]:
    db_results = get_juicing_results(db, stage_id)
    if db_results:
        update_data = results_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_results, field, value)
        db.commit()
        db.refresh(db_results)
    return db_results

def delete_juicing_results(
    db: Session,
    stage_id: int
) -> bool:
    db_results = get_juicing_results(db, stage_id)
    if db_results:
        db.delete(db_results)
        db.commit()
        return True
    return False

# Fermentation Results CRUD operations
def create_fermentation_results(
    db: Session,
    results: FermentationResultsCreate
) -> FermentationResults:
    db_results = FermentationResults(**results.model_dump())
    db.add(db_results)
    db.commit()
    db.refresh(db_results)
    return db_results

def get_fermentation_results(
    db: Session,
    stage_id: int
) -> Optional[FermentationResults]:
    return db.query(FermentationResults).filter(
        FermentationResults.transformation_stage_id == stage_id
    ).first()

def update_fermentation_results(
    db: Session,
    stage_id: int,
    results_update: FermentationResultsUpdate
) -> Optional[FermentationResults]:
    db_results = get_fermentation_results(db, stage_id)
    if db_results:
        update_data = results_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_results, field, value)
        db.commit()
        db.refresh(db_results)
    return db_results

def delete_fermentation_results(
    db: Session,
    stage_id: int
) -> bool:
    db_results = get_fermentation_results(db, stage_id)
    if db_results:
        db.delete(db_results)
        db.commit()
        return True
    return False

# Combined operations
def get_transformation_stage_with_results(
    db: Session,
    stage_id: int
) -> Optional[TransformationStage]:
    return db.query(TransformationStage).filter(
        TransformationStage.id == stage_id
    ).options(
        db.joinedload(TransformationStage.juicing_results),
        db.joinedload(TransformationStage.fermentation_results)
    ).first() 