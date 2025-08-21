from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DistillationLadderBase(BaseModel):
    batch_id: int
    stage: int
    temperature: float
    pressure: float
    alcohol_content: float
    volume: float
    notes: Optional[str] = None

class DistillationLadderCreate(DistillationLadderBase):
    pass

class DistillationLadderUpdate(DistillationLadderBase):
    batch_id: Optional[int] = None
    stage: Optional[int] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    alcohol_content: Optional[float] = None
    volume: Optional[float] = None

class DistillationLadderInDB(DistillationLadderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DistillationLadder(DistillationLadderInDB):
    pass 