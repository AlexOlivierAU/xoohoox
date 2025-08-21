from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_maintenance_log
from app.schemas.maintenance_log import (
    MaintenanceLog,
    MaintenanceLogCreate,
    MaintenanceLogUpdate,
)
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[MaintenanceLog])
def read_maintenance_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Retrieve maintenance logs.
    """
    maintenance_logs = crud_maintenance_log.maintenance_log.get_multi(
        db, skip=skip, limit=limit
    )
    return maintenance_logs

@router.post("/", response_model=MaintenanceLog)
def create_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    maintenance_log_in: MaintenanceLogCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Create new maintenance log.
    """
    maintenance_log = crud_maintenance_log.maintenance_log.create(db=db, obj_in=maintenance_log_in)
    return maintenance_log

@router.put("/{maintenance_log_id}", response_model=MaintenanceLog)
def update_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    maintenance_log_id: int,
    maintenance_log_in: MaintenanceLogUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Update a maintenance log.
    """
    maintenance_log = crud_maintenance_log.maintenance_log.get(db=db, id=maintenance_log_id)
    if not maintenance_log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    maintenance_log = crud_maintenance_log.maintenance_log.update(
        db=db, db_obj=maintenance_log, obj_in=maintenance_log_in
    )
    return maintenance_log

@router.get("/{maintenance_log_id}", response_model=MaintenanceLog)
def read_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    maintenance_log_id: int,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Get maintenance log by ID.
    """
    maintenance_log = crud_maintenance_log.maintenance_log.get(db=db, id=maintenance_log_id)
    if not maintenance_log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return maintenance_log

@router.delete("/{maintenance_log_id}", response_model=MaintenanceLog)
def delete_maintenance_log(
    *,
    db: Session = Depends(deps.get_db),
    maintenance_log_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Delete a maintenance log.
    """
    maintenance_log = crud_maintenance_log.maintenance_log.get(db=db, id=maintenance_log_id)
    if not maintenance_log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    maintenance_log = crud_maintenance_log.maintenance_log.remove(db=db, id=maintenance_log_id)
    return maintenance_log

@router.get("/maintenance/{maintenance_id}", response_model=List[MaintenanceLog])
def read_maintenance_logs_by_maintenance(
    *,
    db: Session = Depends(deps.get_db),
    maintenance_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Retrieve maintenance logs by maintenance ID.
    """
    maintenance_logs = crud_maintenance_log.maintenance_log.get_by_maintenance(
        db=db, maintenance_id=maintenance_id, skip=skip, limit=limit
    )
    return maintenance_logs

@router.get("/technician/{technician_id}", response_model=List[MaintenanceLog])
def read_maintenance_logs_by_technician(
    *,
    db: Session = Depends(deps.get_db),
    technician_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Retrieve maintenance logs by technician ID.
    """
    maintenance_logs = crud_maintenance_log.maintenance_log.get_by_technician(
        db=db, technician_id=technician_id, skip=skip, limit=limit
    )
    return maintenance_logs 