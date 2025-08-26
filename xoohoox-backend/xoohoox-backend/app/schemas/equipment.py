from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import EquipmentType, EquipmentStatus

class EquipmentBase(BaseModel):
    name: str
    type: EquipmentType
    status: EquipmentStatus = EquipmentStatus.OPERATIONAL
    capacity: Optional[float] = None
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    installation_date: Optional[datetime] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    is_critical: bool = False
    location: Optional[str] = None
    notes: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(EquipmentBase):
    name: Optional[str] = None
    type: Optional[EquipmentType] = None
    status: Optional[EquipmentStatus] = None
    is_critical: Optional[bool] = None

class EquipmentResponse(EquipmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EquipmentList(BaseModel):
    items: list[EquipmentResponse]
    total: int
    skip: int
    limit: int
