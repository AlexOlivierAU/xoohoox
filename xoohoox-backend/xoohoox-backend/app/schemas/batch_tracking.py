from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

from app.models.enums import BatchStatus, FruitType, JuiceType, ProcessStatus

class BatchBase(BaseModel):
    batch_id: Optional[str] = None
    name: str
    fruit_type: FruitType
    process_type: str
    grower_id: Optional[str] = None
    status: str = "planned"
    stage: str = "initial"
    progress: float = 0.0
    start_date: datetime
    end_date: datetime

class BatchTrackingCreate(BatchBase):
    @field_validator('batch_id')
    def validate_batch_id(cls, v):
        if v is not None and not v:  # Allow None but not empty string
            raise ValueError("Batch ID cannot be empty")
        return v

class BatchTrackingUpdate(BatchBase):
    batch_id: Optional[str] = None
    name: Optional[str] = None
    fruit_type: Optional[FruitType] = None
    process_type: Optional[str] = None
    status: Optional[str] = None
    stage: Optional[str] = None
    progress: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class BatchTrackingInDB(BatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BatchTrackingResponse(BatchTrackingInDB):
    quality_checks: List[dict] = []
    maintenance_records: List[dict] = []
    environmental_impact: Optional[dict] = None
    processing_start_date: Optional[datetime] = None
    processing_end_date: Optional[datetime] = None
    final_product_quantity: Optional[float] = None
    production_date: Optional[datetime] = None
    recipe_id: Optional[int] = None
    ingredients: List[dict] = []

    class Config:
        from_attributes = True

class BatchTrackingList(BaseModel):
    total: int
    items: List[BatchTrackingResponse]

class StartProduction(BaseModel):
    operator: str
    equipment_id: str

class CompleteProduction(BaseModel):
    final_quantity: float
    quality_grade: str
    notes: Optional[str] = None

class QualityCheckResult(BaseModel):
    test_type: str
    result: str
    value: float
    notes: Optional[str] = None

class ReportIssue(BaseModel):
    issue_type: str
    description: str
    severity: str
    reported_by: str

class TakeCorrectiveAction(BaseModel):
    action_taken: str
    performed_by: str
    result: str
    notes: Optional[str] = None 