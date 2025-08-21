from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.upscale import UpscaleStage, UpscaleStatus

class UpscaleRunBase(BaseModel):
    trial_id: int
    stage: UpscaleStage
    volume: float = Field(..., description="Volume in Liters")
    yield_amount: Optional[float] = Field(None, description="Yield in mL or L")
    abv_result: Optional[float] = Field(None, description="ABV percentage")
    compound_summary: Optional[str] = None
    status: UpscaleStatus = UpscaleStatus.PENDING

class UpscaleRunCreate(UpscaleRunBase):
    pass

class UpscaleRunUpdate(BaseModel):
    yield_amount: Optional[float] = None
    abv_result: Optional[float] = None
    compound_summary: Optional[str] = None
    status: Optional[UpscaleStatus] = None

class UpscaleRunInDB(UpscaleRunBase):
    id: int
    upscale_id: str
    timestamp: datetime

    class Config:
        orm_mode = True 