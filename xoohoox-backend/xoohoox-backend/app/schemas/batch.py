from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from app.models.enums import BatchStatus, FruitType, JuiceType
from .chemistry_adjustment import ChemistryAdjustment
from .fermentation_kinetics import FermentationKinetics
from .distillation_ladder import DistillationLadder
from .trial import Trial
from .environmental_impact import EnvironmentalImpact

class BatchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    fruit_type: FruitType
    juice_type: JuiceType
    target_volume: float = Field(..., gt=0)
    notes: Optional[str] = None
    batch_metadata: Optional[Dict[str, Any]] = None

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[BatchStatus] = None
    actual_volume: Optional[float] = Field(None, ge=0)
    end_date: Optional[datetime] = None
    notes: Optional[str] = None
    batch_metadata: Optional[Dict[str, Any]] = None
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError("End date cannot be before start date")
        return v

class BatchInDB(BatchBase):
    id: int
    status: BatchStatus
    start_date: datetime
    end_date: Optional[datetime] = None
    actual_volume: Optional[float] = None
    
    class Config:
        from_attributes = True

class BatchResponse(BatchInDB):
    pass

class BatchWithRelations(BatchInDB):
    chemistry_adjustments: List[ChemistryAdjustment] = []
    fermentation_kinetics: List[FermentationKinetics] = []
    distillation_ladder: Optional[DistillationLadder] = None
    trials: List[Trial] = []
    environmental_impact: Optional[EnvironmentalImpact] = None

    class Config:
        orm_mode = True 