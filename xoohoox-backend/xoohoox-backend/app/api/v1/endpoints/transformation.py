from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import transformation as crud
from app.schemas.transformation import (
    TransformationStageCreate,
    TransformationStageUpdate,
    TransformationStage,
    JuicingResultsCreate,
    JuicingResultsUpdate,
    JuicingResults,
    FermentationResultsCreate,
    FermentationResultsUpdate,
    FermentationResults,
    TransformationStageWithResults
)

router = APIRouter()

# Transformation Stage endpoints
@router.post("/stages/", response_model=TransformationStage)
def create_transformation_stage(
    *,
    db: Session = Depends(deps.get_db),
    stage_in: TransformationStageCreate,
    current_user = Depends(deps.get_current_active_user)
):
    stage = crud.create_transformation_stage(db=db, stage=stage_in)
    return stage

@router.get("/stages/", response_model=List[TransformationStage])
def read_transformation_stages(
    db: Session = Depends(deps.get_db),
    batch_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(deps.get_current_active_user)
):
    stages = crud.get_transformation_stages(
        db=db,
        batch_id=batch_id,
        skip=skip,
        limit=limit
    )
    return stages

@router.get("/stages/{stage_id}", response_model=TransformationStageWithResults)
def read_transformation_stage(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    stage = crud.get_transformation_stage_with_results(db=db, stage_id=stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Transformation stage not found")
    return stage

@router.put("/stages/{stage_id}", response_model=TransformationStage)
def update_transformation_stage(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    stage_in: TransformationStageUpdate,
    current_user = Depends(deps.get_current_active_user)
):
    stage = crud.update_transformation_stage(
        db=db,
        stage_id=stage_id,
        stage_update=stage_in
    )
    if not stage:
        raise HTTPException(status_code=404, detail="Transformation stage not found")
    return stage

@router.delete("/stages/{stage_id}")
def delete_transformation_stage(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    success = crud.delete_transformation_stage(db=db, stage_id=stage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transformation stage not found")
    return {"message": "Transformation stage deleted successfully"}

# Juicing Results endpoints
@router.post("/stages/{stage_id}/juicing", response_model=JuicingResults)
def create_juicing_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    results_in: JuicingResultsCreate,
    current_user = Depends(deps.get_current_active_user)
):
    # Verify stage exists
    stage = crud.get_transformation_stage(db=db, stage_id=stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Transformation stage not found")
    
    results = crud.create_juicing_results(db=db, results=results_in)
    return results

@router.get("/stages/{stage_id}/juicing", response_model=JuicingResults)
def read_juicing_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    results = crud.get_juicing_results(db=db, stage_id=stage_id)
    if not results:
        raise HTTPException(status_code=404, detail="Juicing results not found")
    return results

@router.put("/stages/{stage_id}/juicing", response_model=JuicingResults)
def update_juicing_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    results_in: JuicingResultsUpdate,
    current_user = Depends(deps.get_current_active_user)
):
    results = crud.update_juicing_results(
        db=db,
        stage_id=stage_id,
        results_update=results_in
    )
    if not results:
        raise HTTPException(status_code=404, detail="Juicing results not found")
    return results

@router.delete("/stages/{stage_id}/juicing")
def delete_juicing_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    success = crud.delete_juicing_results(db=db, stage_id=stage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Juicing results not found")
    return {"message": "Juicing results deleted successfully"}

# Fermentation Results endpoints
@router.post("/stages/{stage_id}/fermentation", response_model=FermentationResults)
def create_fermentation_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    results_in: FermentationResultsCreate,
    current_user = Depends(deps.get_current_active_user)
):
    # Verify stage exists
    stage = crud.get_transformation_stage(db=db, stage_id=stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Transformation stage not found")
    
    results = crud.create_fermentation_results(db=db, results=results_in)
    return results

@router.get("/stages/{stage_id}/fermentation", response_model=FermentationResults)
def read_fermentation_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    results = crud.get_fermentation_results(db=db, stage_id=stage_id)
    if not results:
        raise HTTPException(status_code=404, detail="Fermentation results not found")
    return results

@router.put("/stages/{stage_id}/fermentation", response_model=FermentationResults)
def update_fermentation_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    results_in: FermentationResultsUpdate,
    current_user = Depends(deps.get_current_active_user)
):
    results = crud.update_fermentation_results(
        db=db,
        stage_id=stage_id,
        results_update=results_in
    )
    if not results:
        raise HTTPException(status_code=404, detail="Fermentation results not found")
    return results

@router.delete("/stages/{stage_id}/fermentation")
def delete_fermentation_results(
    *,
    db: Session = Depends(deps.get_db),
    stage_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    success = crud.delete_fermentation_results(db=db, stage_id=stage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fermentation results not found")
    return {"message": "Fermentation results deleted successfully"} 