from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import batch_tracking, quality_control, equipment_maintenance
from app.models.enums import BatchStatus, JuiceType
from app.services.batch_number import BatchNumberGenerator
from app.schemas.batch_tracking import (
    BatchTrackingCreate,
    BatchTrackingUpdate,
    BatchTrackingResponse,
    BatchTrackingList,
    StartProduction,
    CompleteProduction,
    QualityCheckResult,
    ReportIssue,
    TakeCorrectiveAction,
)
from app.schemas.quality_control import QualityControlResponse, QualityControlCreate
from app.schemas.equipment_maintenance import EquipmentMaintenanceResponse, EquipmentMaintenanceCreate

router = APIRouter()

@router.post("/", response_model=BatchTrackingResponse)
def create_batch(
    *,
    db: Session = Depends(deps.get_db),
    batch_in: BatchTrackingCreate,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Create new batch.
    """
    # Generate a unique batch ID if not provided
    if not batch_in.batch_id:
        batch_in.batch_id = BatchNumberGenerator.generate_batch_id(
            db=db,
            fruit_type=batch_in.fruit_type,
            process_type=batch_in.process_type,
            grower_id=batch_in.grower_id if hasattr(batch_in, 'grower_id') else None
        )
    else:
        # Validate the provided batch ID
        if not BatchNumberGenerator.validate_batch_id(batch_in.batch_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid batch ID format. Expected format: [GROWER-]YYMMDD-FT-PT-XXX",
            )
    
    # Check if batch already exists
    existing_batch = batch_tracking.get_by_batch_id(db, batch_id=batch_in.batch_id)
    if existing_batch:
        raise HTTPException(
            status_code=400,
            detail="A batch with this ID already exists.",
        )
    
    batch = batch_tracking.create(db, obj_in=batch_in)
    return batch

@router.get("/", response_model=BatchTrackingList)
def read_batches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    juice_type: Optional[JuiceType] = None,
    status: Optional[BatchStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingList:
    """
    Retrieve batches.
    """
    batches = batch_tracking.get_multi(
        db,
        skip=skip,
        limit=limit,
        juice_type=juice_type,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )
    total = len(batches)  # In a real app, you'd want to get this from the database
    return BatchTrackingList(total=total, items=batches)

@router.get("/{batch_id}", response_model=BatchTrackingResponse)
def read_batch(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Get batch by ID.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    return batch

@router.put("/{batch_id}", response_model=BatchTrackingResponse)
def update_batch(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    batch_in: BatchTrackingUpdate,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Update a batch.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    batch = batch_tracking.update(db, db_obj=batch, obj_in=batch_in)
    return batch

@router.post("/{batch_id}/start", response_model=BatchTrackingResponse)
def start_batch_production(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    data: StartProduction,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Start production of a batch.
    """
    try:
        batch = batch_tracking.start_production(db, batch_id=batch_id, data=data)
        if not batch:
            raise HTTPException(
                status_code=404,
                detail="Batch not found",
            )
        return batch
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/{batch_id}/complete", response_model=BatchTrackingResponse)
def complete_batch_production(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    data: CompleteProduction,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Complete production of a batch.
    """
    try:
        batch = batch_tracking.complete_production(db, batch_id=batch_id, data=data)
        if not batch:
            raise HTTPException(
                status_code=404,
                detail="Batch not found",
            )
        return batch
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/{batch_id}/quality-check", response_model=BatchTrackingResponse)
def record_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    data: QualityCheckResult,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Record quality check results for a batch.
    """
    try:
        batch = batch_tracking.record_quality_check(db, batch_id=batch_id, data=data)
        if not batch:
            raise HTTPException(
                status_code=404,
                detail="Batch not found",
            )
        return batch
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/{batch_id}/issues", response_model=BatchTrackingResponse)
def report_batch_issue(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    data: ReportIssue,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Report an issue with a batch.
    """
    batch = batch_tracking.report_issue(db, batch_id=batch_id, data=data)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    return batch

@router.post("/{batch_id}/corrective-actions", response_model=BatchTrackingResponse)
def take_corrective_action(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    data: TakeCorrectiveAction,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Record a corrective action for a batch issue.
    """
    batch = batch_tracking.take_corrective_action(db, batch_id=batch_id, data=data)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    return batch

@router.delete("/{batch_id}", response_model=BatchTrackingResponse)
def delete_batch(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    current_user: str = Depends(deps.get_current_user),
) -> BatchTrackingResponse:
    """
    Delete a batch.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    batch = batch_tracking.remove(db, id=batch.id)
    return batch

@router.get("/")
def get_batches():
    return {"message": "List of batches"}

@router.get("/{batch_id}/quality-checks", response_model=List[QualityControlResponse])
def get_batch_quality_checks(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(deps.get_current_user),
) -> List[QualityControlResponse]:
    """
    Get quality checks for a batch.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    quality_checks = quality_control.get_multi(
        db, skip=skip, limit=limit, batch_id=batch_id
    )
    return quality_checks

@router.post("/{batch_id}/quality-checks", response_model=QualityControlResponse)
def add_batch_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    quality_check_in: QualityControlCreate,
    current_user: str = Depends(deps.get_current_user),
) -> QualityControlResponse:
    """
    Add a quality check to a batch.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    quality_check = quality_control.create(db, obj_in=quality_check_in)
    return quality_check

@router.get("/{batch_id}/maintenance", response_model=List[EquipmentMaintenanceResponse])
def get_batch_maintenance(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(deps.get_current_user),
) -> List[EquipmentMaintenanceResponse]:
    """
    Get maintenance records for a batch.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    maintenance_records = equipment_maintenance.get_multi(
        db, skip=skip, limit=limit, batch_id=batch_id
    )
    return maintenance_records

@router.post("/{batch_id}/maintenance", response_model=EquipmentMaintenanceResponse)
def add_batch_maintenance(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    maintenance_in: EquipmentMaintenanceCreate,
    current_user: str = Depends(deps.get_current_user),
) -> EquipmentMaintenanceResponse:
    """
    Add a maintenance record to a batch.
    """
    batch = batch_tracking.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found",
        )
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    return maintenance 