from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class BatchDispatchBase(BaseModel):
    batch_id: str
    grower_id: int
    produce_type: str
    varietal: str
    dispatch_date: date
    quantity_kg: float = Field(gt=0)

class BatchDispatchCreate(BatchDispatchBase):
    pass

class BatchDispatchUpdate(BaseModel):
    batch_id: Optional[str] = None
    grower_id: Optional[int] = None
    produce_type: Optional[str] = None
    varietal: Optional[str] = None
    dispatch_date: Optional[date] = None
    quantity_kg: Optional[float] = Field(None, gt=0)

class BatchDispatch(BatchDispatchBase):
    id: int

    class Config:
        from_attributes = True 