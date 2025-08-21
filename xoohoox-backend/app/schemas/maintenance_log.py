from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MaintenanceLogBase(BaseModel):
    maintenance_id: int
    technician_id: int
    action_taken: str
    notes: Optional[str] = None
    parts_replaced: Optional[str] = None
    cost: Optional[float] = None

class MaintenanceLogCreate(MaintenanceLogBase):
    pass

class MaintenanceLogUpdate(BaseModel):
    action_taken: Optional[str] = None
    notes: Optional[str] = None
    parts_replaced: Optional[str] = None
    cost: Optional[float] = None

class MaintenanceLogInDB(MaintenanceLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MaintenanceLog(MaintenanceLogInDB):
    pass 