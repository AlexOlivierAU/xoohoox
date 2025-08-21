from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.maintenance_log import maintenance_log
from app.schemas.maintenance_log import (
    MaintenanceLogCreate,
    MaintenanceLogUpdate,
    MaintenanceLogResponse
)

router = APIRouter()

@router.post("/", response_model=MaintenanceLogResponse)
def create_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    maintenance_log_in: MaintenanceLogCreate,
) -> MaintenanceLogResponse:
    """
    Create a new maintenance log entry.
    """
    log = maintenance_log.create(db=db, obj_in=maintenance_log_in)
    return log

@router.get("/", response_model=List[MaintenanceLogResponse])
def read_maintenance_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    maintenance_id: Optional[int] = None,
    performed_by: Optional[str] = None,
) -> List[MaintenanceLogResponse]:
    """
    Retrieve maintenance log entries.
    """
    if maintenance_id:
        logs = maintenance_log.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    elif performed_by:
        logs = maintenance_log.get_by_performed_by(db=db, performed_by=performed_by)
    else:
        logs = maintenance_log.get_multi(db=db, skip=skip, limit=limit)
    return logs

@router.get("/{log_id}", response_model=MaintenanceLogResponse)
def read_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    log_id: int,
) -> MaintenanceLogResponse:
    """
    Get a specific maintenance log entry by ID.
    """
    log = maintenance_log.get(db=db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return log

@router.put("/{log_id}", response_model=MaintenanceLogResponse)
def update_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    log_id: int,
    maintenance_log_in: MaintenanceLogUpdate,
) -> MaintenanceLogResponse:
    """
    Update a maintenance log entry.
    """
    log = maintenance_log.get(db=db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    log = maintenance_log.update(db=db, db_obj=log, obj_in=maintenance_log_in)
    return log

@router.delete("/{log_id}", response_model=MaintenanceLogResponse)
def delete_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    log_id: int,
) -> MaintenanceLogResponse:
    """
    Delete a maintenance log entry.
    """
    log = maintenance_log.get(db=db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    log = maintenance_log.remove(db=db, id=log_id)
    return log

@router.get("/")
def list_logs(current_user: str = Depends(deps.get_current_user)):
    """
    List all maintenance logs.
    """
    # Return dummy data for now
    return [
        {
            "id": 1,
            "equipment_id": "E001",
            "maintenance_id": 1,
            "notes": "Regular cleaning completed",
            "date": "2024-01-20"
        }
    ] 