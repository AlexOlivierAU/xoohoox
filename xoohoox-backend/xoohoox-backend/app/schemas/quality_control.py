from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class TestType(str, Enum):
    MICROBIAL = "MICROBIAL"
    CHEMICAL = "CHEMICAL"
    PHYSICAL = "PHYSICAL"
    SENSORY = "SENSORY"
    OTHER = "OTHER"

class TestResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PENDING = "PENDING"
    INCONCLUSIVE = "INCONCLUSIVE"

# Base schema with common attributes
class QualityControlBase(BaseModel):
    test_id: str = Field(..., description="Unique identifier for the test")
    batch_id: str = Field(..., description="Reference to the batch being tested")
    test_type: TestType = Field(..., description="Type of test being performed")
    test_date: datetime = Field(..., description="Date when the test was performed")
    test_name: str = Field(..., description="Name of the specific test")
    test_method: str = Field(..., description="Method used for the test")
    test_parameters: Optional[str] = Field(None, description="Parameters used in the test")
    expected_range_min: Optional[float] = Field(None, description="Minimum expected value")
    expected_range_max: Optional[float] = Field(None, description="Maximum expected value")
    actual_value: Optional[float] = Field(None, description="Actual value measured")
    unit_of_measure: str = Field(..., description="Unit of measurement for the test")
    result: TestResult = Field(..., description="Result of the test")
    tester_id: str = Field(..., description="ID of the person who performed the test")
    equipment_used: Optional[str] = Field(None, description="Equipment used for the test")
    temperature_c: Optional[float] = Field(None, ge=-50, le=100, description="Temperature during the test in Celsius")
    humidity_percent: Optional[float] = Field(None, ge=0, le=100, description="Humidity during the test in percent")
    notes: Optional[str] = Field(None, description="Additional notes about the test")
    corrective_actions: Optional[str] = Field(None, description="Actions taken if test failed")
    retest_required: bool = Field(False, description="Whether a retest is required")

    @validator('expected_range_max')
    def validate_range(cls, v, values):
        if v and 'expected_range_min' in values and values['expected_range_min'] is not None:
            if v < values['expected_range_min']:
                raise ValueError("Maximum expected value must be greater than minimum expected value")
        return v

    @validator('test_date')
    def validate_test_date(cls, v):
        if v > datetime.now():
            raise ValueError("Test date cannot be in the future")
        return v

    @validator('batch_id')
    def validate_batch_id(cls, v):
        # TODO: Add actual batch validation when batch service is implemented
        if not v or len(v.strip()) == 0:
            raise ValueError("Batch ID cannot be empty")
        return v

    @validator('tester_id')
    def validate_tester_id(cls, v):
        # TODO: Add actual user validation when user service is implemented
        if not v or len(v.strip()) == 0:
            raise ValueError("Tester ID cannot be empty")
        return v

# Schema for creating a new quality control test
class QualityControlCreate(QualityControlBase):
    pass

# Schema for updating an existing quality control test
class QualityControlUpdate(BaseModel):
    test_type: Optional[TestType] = None
    test_date: Optional[datetime] = None
    test_name: Optional[str] = None
    test_method: Optional[str] = None
    test_parameters: Optional[str] = None
    expected_range_min: Optional[float] = None
    expected_range_max: Optional[float] = None
    actual_value: Optional[float] = None
    unit_of_measure: Optional[str] = None
    result: Optional[TestResult] = None
    tester_id: Optional[str] = None
    equipment_used: Optional[str] = None
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    notes: Optional[str] = None
    corrective_actions: Optional[str] = None
    retest_required: Optional[bool] = None

    @validator('expected_range_max')
    def validate_range(cls, v, values):
        if v and 'expected_range_min' in values and values['expected_range_min'] is not None:
            if v < values['expected_range_min']:
                raise ValueError("Maximum expected value must be greater than minimum expected value")
        return v

# Schema for quality control test response
class QualityControlResponse(QualityControlBase):
    id: int = Field(..., description="Database ID of the test")
    created_at: datetime = Field(..., description="Timestamp when the test was created")
    updated_at: datetime = Field(..., description="Timestamp when the test was last updated")

    class Config:
        orm_mode = True

# Schema for quality control test list response
class QualityControlList(BaseModel):
    items: List[QualityControlResponse]
    total: int
    page: int
    size: int
    pages: int 