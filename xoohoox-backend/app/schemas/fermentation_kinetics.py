from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class FermentationKineticsBase(BaseModel):
    batch_id: int
    temperature: float
    ph: float
    brix: float
    alcohol_content: float
    yeast_strain: str
    inoculation_rate: float
    notes: Optional[str] = None

class FermentationKineticsCreate(FermentationKineticsBase):
    pass

class FermentationKineticsUpdate(FermentationKineticsBase):
    batch_id: Optional[int] = None
    temperature: Optional[float] = None
    ph: Optional[float] = None
    brix: Optional[float] = None
    alcohol_content: Optional[float] = None
    yeast_strain: Optional[str] = None
    inoculation_rate: Optional[float] = None

class FermentationKineticsInDB(FermentationKineticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FermentationKinetics(FermentationKineticsInDB):
    pass 