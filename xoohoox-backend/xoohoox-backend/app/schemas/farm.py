from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class FarmBase(BaseModel):
    name: str
    location: str
    contact_info: Optional[str] = None
    notes: Optional[str] = None

class FarmCreate(FarmBase):
    pass

class FarmUpdate(FarmBase):
    name: Optional[str] = None
    location: Optional[str] = None

class Farm(FarmBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 