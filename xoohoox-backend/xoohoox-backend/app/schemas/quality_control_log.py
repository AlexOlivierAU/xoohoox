from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class QualityControlLogBase(BaseModel):
    batch_id: int
    test_date: datetime
    brix: Optional[float] = Field(gt=0)
    ph: Optional[float] = Field(gt=0)
    alcohol_content: Optional[float] = Field(gt=0)
    acidity: Optional[float] = Field(gt=0)
    temperature: Optional[float] = None
    appearance: Optional[str] = None
    aroma: Optional[str] = None
    taste: Optional[str] = None
    overall_quality: Optional[str] = None
    passed_quality_check: bool
    notes: Optional[str] = None

class QualityControlLogCreate(QualityControlLogBase):
    pass

class QualityControlLogUpdate(QualityControlLogBase):
    batch_id: Optional[int] = None
    test_date: Optional[datetime] = None
    passed_quality_check: Optional[bool] = None

class QualityControlLog(QualityControlLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 