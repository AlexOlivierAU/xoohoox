from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator

class MaintenanceBase(BaseModel):
    equipment_id: int
    maintenance_type: str
    description: str
    scheduled_date: datetime
    priority: str
    status: str
    notes: Optional[str] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(MaintenanceBase):
    equipment_id: Optional[int] = None
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class Maintenance(MaintenanceBase):
    id: int
    completion_date: Optional[datetime] = None
    performed_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

    @field_validator('scheduled_date')
    def validate_scheduled_date(cls, v):
        if v < datetime.now():
            raise ValueError('Scheduled date cannot be in the past')
        return v

    @field_validator('completion_date')
    def validate_completion_date(cls, v, values):
        if v and values.get('scheduled_date') and v < values['scheduled_date']:
            raise ValueError('Completion date cannot be before scheduled date')
        return v

    @field_validator('equipment_id')
    def validate_equipment_id(cls, v):
        if v <= 0:
            raise ValueError('Equipment ID must be greater than 0')
        return v 