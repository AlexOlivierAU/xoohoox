from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas import (
    EquipmentMaintenanceCreate,
    EquipmentMaintenanceUpdate,
    EquipmentMaintenanceResponse,
    EquipmentMaintenanceList,
    MaintenanceType,
    MaintenanceStatus,
    EquipmentType
)
from app.crud import equipment_maintenance
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=EquipmentMaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_in: EquipmentMaintenanceCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new equipment maintenance record.
    """
    return equipment_maintenance.create(db=db, obj_in=maintenance_in)

@router.get("/", response_model=EquipmentMaintenanceList)
def read_maintenance_records(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    equipment_id: Optional[str] = None,
    maintenance_type: Optional[MaintenanceType] = None,
    maintenance_status: Optional[MaintenanceStatus] = None,
    equipment_type: Optional[EquipmentType] = None,
    is_critical: Optional[bool] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve equipment maintenance records with optional filtering.
    """
    records = equipment_maintenance.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        equipment_id=equipment_id,
        maintenance_type=maintenance_type,
        maintenance_status=maintenance_status,
        equipment_type=equipment_type,
        is_critical=is_critical
    )
    total = equipment_maintenance.count(
        db=db,
        equipment_id=equipment_id,
        maintenance_type=maintenance_type,
        maintenance_status=maintenance_status,
        equipment_type=equipment_type,
        is_critical=is_critical
    )
    pages = (total + limit - 1) // limit
    
    return {
        "items": records,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": pages
    }

@router.get("/{maintenance_id}", response_model=EquipmentMaintenanceResponse)
def read_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific equipment maintenance record by ID.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    return db_maintenance

@router.put("/{maintenance_id}", response_model=EquipmentMaintenanceResponse)
def update_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    maintenance_in: EquipmentMaintenanceUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update an equipment maintenance record.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    return equipment_maintenance.update(db=db, db_obj=db_maintenance, obj_in=maintenance_in)

@router.delete("/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete an equipment maintenance record.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    equipment_maintenance.remove(db=db, id=db_maintenance.id)
    return None

@router.get("/equipment/{equipment_id}", response_model=EquipmentMaintenanceList)
def read_equipment_maintenance(
    *,
    db: Session = Depends(get_db),
    equipment_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get all maintenance records for a specific equipment.
    """
    records = equipment_maintenance.get_multi(
        db=db, skip=skip, limit=limit, equipment_id=equipment_id
    )
    total = equipment_maintenance.count(db=db, equipment_id=equipment_id)
    pages = (total + limit - 1) // limit
    
    return {
        "items": records,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": pages
    }

@router.post("/{maintenance_id}/start", response_model=EquipmentMaintenanceResponse)
def start_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Start a scheduled maintenance.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    
    if db_maintenance.maintenance_status != MaintenanceStatus.SCHEDULED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maintenance must be in scheduled status to start. Current status: {db_maintenance.maintenance_status}"
        )
    
    return equipment_maintenance.start_maintenance(db=db, db_obj=db_maintenance)

@router.post("/{maintenance_id}/complete", response_model=EquipmentMaintenanceResponse)
def complete_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    results: str,
    parts_replaced: Optional[str] = None,
    cost: Optional[float] = None,
    next_maintenance_date: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Complete a maintenance that is in progress.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    
    if db_maintenance.maintenance_status != MaintenanceStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maintenance must be in progress to complete. Current status: {db_maintenance.maintenance_status}"
        )
    
    return equipment_maintenance.complete_maintenance(
        db=db,
        db_obj=db_maintenance,
        results=results,
        parts_replaced=parts_replaced,
        cost=cost,
        next_maintenance_date=next_maintenance_date
    )

@router.post("/{maintenance_id}/delay", response_model=EquipmentMaintenanceResponse)
def delay_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    new_scheduled_date: str,
    reason: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delay a scheduled maintenance.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    
    if db_maintenance.maintenance_status != MaintenanceStatus.SCHEDULED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maintenance must be in scheduled status to delay. Current status: {db_maintenance.maintenance_status}"
        )
    
    return equipment_maintenance.delay_maintenance(
        db=db,
        db_obj=db_maintenance,
        new_scheduled_date=new_scheduled_date,
        reason=reason
    )

@router.post("/{maintenance_id}/cancel", response_model=EquipmentMaintenanceResponse)
def cancel_maintenance(
    *,
    db: Session = Depends(get_db),
    maintenance_id: str,
    reason: str,
    current_user: User = Depends(get_current_user)
):
    """
    Cancel a scheduled maintenance.
    """
    db_maintenance = equipment_maintenance.get_by_maintenance_id(db=db, maintenance_id=maintenance_id)
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance record with ID {maintenance_id} not found"
        )
    
    if db_maintenance.maintenance_status not in [MaintenanceStatus.SCHEDULED, MaintenanceStatus.DELAYED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maintenance must be in scheduled or delayed status to cancel. Current status: {db_maintenance.maintenance_status}"
        )
    
    return equipment_maintenance.cancel_maintenance(
        db=db,
        db_obj=db_maintenance,
        reason=reason
    )

@router.get("/")
def list_maintenance(current_user: str = Depends(get_current_user)):
    """
    List all maintenance records.
    """
    # Return dummy data for now
    return [
        {
            "id": 1,
            "equipment_id": "E001",
            "type": "cleaning",
            "status": "completed",
            "date": "2024-01-20"
        }
    ]

@router.put("/{equipment_id}", response_model=EquipmentMaintenanceResponse)
def update_equipment(
    *,
    db: Session = Depends(get_db),
    equipment_id: str,
    equipment_in: EquipmentMaintenanceUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update equipment details.
    """
    db_equipment = equipment_maintenance.get_by_equipment_id(db=db, equipment_id=equipment_id)
    if not db_equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipment with ID {equipment_id} not found"
        )
    return equipment_maintenance.update(db=db, db_obj=db_equipment, obj_in=equipment_in)

@router.get("/{equipment_id}/maintenance", response_model=EquipmentMaintenanceList)
def get_equipment_maintenance_history(
    *,
    db: Session = Depends(get_db),
    equipment_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get maintenance history for a specific equipment.
    """
    records = equipment_maintenance.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        equipment_id=equipment_id
    )
    total = equipment_maintenance.count(
        db=db,
        equipment_id=equipment_id
    )
    pages = (total + limit - 1) // limit
    
    return {
        "items": records,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": pages
    }

@router.post("/{equipment_id}/maintenance", response_model=EquipmentMaintenanceResponse)
def schedule_maintenance(
    *,
    db: Session = Depends(get_db),
    equipment_id: str,
    maintenance_in: EquipmentMaintenanceCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Schedule maintenance for a specific equipment.
    """
    db_equipment = equipment_maintenance.get_by_equipment_id(db=db, equipment_id=equipment_id)
    if not db_equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipment with ID {equipment_id} not found"
        )
    return equipment_maintenance.create(db=db, obj_in=maintenance_in) 