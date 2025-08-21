from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum

class PathTaken(str, Enum):
    VINEGAR = "vinegar"
    DISTILLATION = "distillation"
    ARCHIVED = "archived"

class JuiceVariant(str, Enum):
    JP1 = "JP1"
    JP2 = "JP2"
    JP3 = "JP3"
    JP4 = "JP4"
    JP5 = "JP5"

class DailyReading(BaseModel):
    timestamp: datetime
    sg: float = Field(..., description="Specific Gravity")
    ph: float
    brix: float
    abv: float
    notes: Optional[str] = None

class UpscaleEvent(BaseModel):
    timestamp: datetime
    test_number: int
    volume: float
    notes: Optional[str] = None

class FermentationTrialBase(BaseModel):
    yeast_strain: str
    juice_variant: JuiceVariant
    initial_volume: float
    sg: Optional[float] = None
    ph: Optional[float] = None
    brix: Optional[float] = None
    current_abv: Optional[float] = None
    status: Optional[str] = "Awaiting"

class FermentationTrialCreate(FermentationTrialBase):
    batch_id: int

class FermentationTrialUpdate(BaseModel):
    yeast_strain: Optional[str] = None
    juice_variant: Optional[JuiceVariant] = None
    initial_volume: Optional[float] = None
    sg: Optional[float] = None
    ph: Optional[float] = None
    brix: Optional[float] = None
    current_abv: Optional[float] = None
    status: Optional[str] = None
    path_taken: Optional[PathTaken] = None

class DailyReadingCreate(BaseModel):
    sg: float
    ph: float
    brix: float
    abv: float
    notes: Optional[str] = None

class UpscaleEventCreate(BaseModel):
    test_number: int
    volume: float
    notes: Optional[str] = None

class FermentationTrialInDB(FermentationTrialBase):
    id: int
    trial_id: str
    batch_id: int
    path_taken: Optional[PathTaken] = None
    daily_readings: List[DailyReading] = []
    upscale_history: List[UpscaleEvent] = []
    compound_results: Dict = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FermentationTrialWithBatch(FermentationTrialInDB):
    batch: "BatchInDB"  # Forward reference to avoid circular import

class FermentationTrialList(BaseModel):
    trials: List[FermentationTrialInDB]
    total: int 