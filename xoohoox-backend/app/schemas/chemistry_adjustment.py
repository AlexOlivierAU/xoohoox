from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ChemistryAdjustmentBase(BaseModel):
    batch_id: int
    ph_adjustment: float
    brix_adjustment: float
    acid_adjustment: float
    sugar_adjustment: float
    notes: Optional[str] = None

class ChemistryAdjustmentCreate(ChemistryAdjustmentBase):
    pass

class ChemistryAdjustmentUpdate(ChemistryAdjustmentBase):
    batch_id: Optional[int] = None
    ph_adjustment: Optional[float] = None
    brix_adjustment: Optional[float] = None
    acid_adjustment: Optional[float] = None
    sugar_adjustment: Optional[float] = None

class ChemistryAdjustmentInDB(ChemistryAdjustmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChemistryAdjustment(ChemistryAdjustmentInDB):
    pass 