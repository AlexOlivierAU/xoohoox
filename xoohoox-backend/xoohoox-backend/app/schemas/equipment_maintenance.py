from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.enums import MaintenanceType, MaintenanceStatus, EquipmentType

# Base schema with common attributes
class EquipmentMaintenanceBase(BaseModel):
    equipment_id: str
    equipment_type: EquipmentType
    maintenance_type: MaintenanceType
    description: str
    technician_id: str
    scheduled_date: datetime
    status: MaintenanceStatus = MaintenanceStatus.SCHEDULED
    performed_by: str
    notes: Optional[str] = None
    batch_id: Optional[str] = None

# Schema for creating a new equipment maintenance record
class EquipmentMaintenanceCreate(EquipmentMaintenanceBase):
    pass

# Schema for updating an existing equipment maintenance record
class EquipmentMaintenanceUpdate(BaseModel):
    equipment_type: Optional[EquipmentType] = None
    maintenance_type: Optional[MaintenanceType] = None
    description: Optional[str] = None
    technician_id: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    status: Optional[MaintenanceStatus] = None
    completion_date: Optional[datetime] = None
    notes: Optional[str] = None

# Schema for equipment maintenance response
class EquipmentMaintenanceResponse(EquipmentMaintenanceBase):
    id: int
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema for equipment maintenance list response
class EquipmentMaintenanceList(BaseModel):
    total: int
    items: List[EquipmentMaintenanceResponse] 