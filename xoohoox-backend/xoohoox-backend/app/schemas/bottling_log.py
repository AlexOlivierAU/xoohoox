from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class BottlingLogBase(BaseModel):
    batch_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    initial_volume: float = Field(gt=0)
    final_volume: Optional[float] = Field(gt=0)
    brix: Optional[float] = Field(gt=0)
    ph: Optional[float] = Field(gt=0)
    temperature: Optional[float] = None
    bottle_size: Optional[str] = None
    bottle_count: Optional[int] = Field(gt=0)
    notes: Optional[str] = None

class BottlingLogCreate(BottlingLogBase):
    pass

class BottlingLogUpdate(BottlingLogBase):
    batch_id: Optional[int] = None
    start_time: Optional[datetime] = None
    initial_volume: Optional[float] = Field(gt=0)
    bottle_size: Optional[str] = None
    bottle_count: Optional[int] = Field(gt=0)

class BottlingLog(BottlingLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 