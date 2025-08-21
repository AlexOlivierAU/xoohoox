from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.enums import MaintenanceType, MaintenanceStatus

class MaintenanceLogBase(BaseModel):
    equipment_id: str
    maintenance_type: MaintenanceType
    description: str
    status: MaintenanceStatus = MaintenanceStatus.SCHEDULED
    scheduled_date: datetime
    completion_date: Optional[datetime] = None
    notes: Optional[str] = None
    technician_id: Optional[str] = None

class MaintenanceLogCreate(MaintenanceLogBase):
    pass

class MaintenanceLogUpdate(BaseModel):
    maintenance_type: Optional[MaintenanceType] = None
    description: Optional[str] = None
    status: Optional[MaintenanceStatus] = None
    scheduled_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    notes: Optional[str] = None
    technician_id: Optional[str] = None

class MaintenanceLogResponse(MaintenanceLogBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MaintenanceLogList(BaseModel):
    items: list[MaintenanceLogResponse]
    total: int 