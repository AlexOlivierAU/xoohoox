from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class JuicingLogBase(BaseModel):
    batch_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    initial_volume: float = Field(gt=0)
    final_volume: Optional[float] = Field(gt=0)
    brix: Optional[float] = Field(gt=0)
    ph: Optional[float] = Field(gt=0)
    temperature: Optional[float] = None
    notes: Optional[str] = None

class JuicingLogCreate(JuicingLogBase):
    pass

class JuicingLogUpdate(JuicingLogBase):
    batch_id: Optional[int] = None
    start_time: Optional[datetime] = None
    initial_volume: Optional[float] = Field(gt=0)

class JuicingLog(JuicingLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 