from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TrialBase(BaseModel):
    batch_id: int
    name: str
    description: Optional[str] = None
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None
    results: Optional[dict] = None
    notes: Optional[str] = None

class TrialCreate(TrialBase):
    pass

class TrialUpdate(TrialBase):
    batch_id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    results: Optional[dict] = None

class TrialInDB(TrialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Trial(TrialInDB):
    pass 