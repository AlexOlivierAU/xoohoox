from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.enums import QualityTestType, TestResult

class QualityTestBase(BaseModel):
    batch_id: int
    test_type: QualityTestType
    test_date: datetime
    result: TestResult
    measured_value: float
    expected_range_min: float
    expected_range_max: float
    tester_id: int
    notes: Optional[str] = None

class QualityTestCreate(QualityTestBase):
    pass

class QualityTestUpdate(QualityTestBase):
    batch_id: Optional[int] = None
    test_type: Optional[QualityTestType] = None
    test_date: Optional[datetime] = None
    result: Optional[TestResult] = None
    measured_value: Optional[float] = None
    expected_range_min: Optional[float] = None
    expected_range_max: Optional[float] = None
    tester_id: Optional[int] = None

class QualityTest(QualityTestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

    @field_validator('expected_range_max')
    def validate_range(cls, v, values):
        if 'expected_range_min' in values and v < values['expected_range_min']:
            raise ValueError('Maximum range must be greater than minimum range')
        return v

    @field_validator('test_date')
    def validate_test_date(cls, v):
        if v > datetime.now():
            raise ValueError('Test date cannot be in the future')
        return v

    @field_validator('batch_id')
    def validate_batch_id(cls, v):
        if v <= 0:
            raise ValueError('Batch ID must be greater than 0')
        return v

    @field_validator('tester_id')
    def validate_tester_id(cls, v):
        if v <= 0:
            raise ValueError('Tester ID must be greater than 0')
        return v 