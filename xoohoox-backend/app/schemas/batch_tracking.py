from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class BatchBase(BaseModel):
    fruit_type: str
    apple_variety: Optional[str] = None
    target_quantity: float
    notes: Optional[str] = None

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BatchBase):
    fruit_type: Optional[str] = None
    target_quantity: Optional[float] = None

class BatchInDB(BatchBase):
    id: int
    actual_quantity: Optional[float] = None
    status: str
    fermentation_stage: str
    distillation_stage: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BatchWithRelations(BatchInDB):
    quality_checks: List[dict] = []
    maintenance_records: List[dict] = []
    environmental_impact: Optional[dict] = None
    processing_start_date: Optional[datetime] = None
    processing_end_date: Optional[datetime] = None
    final_product_quantity: Optional[float] = None
    production_date: Optional[datetime] = None
    recipe_id: Optional[int] = None
    ingredients: List[dict] = []

    model_config = {
        "from_attributes": True
    }

    @field_validator('processing_end_date')
    def validate_processing_end_date(cls, v, values):
        if v and values.get('processing_start_date') and v < values['processing_start_date']:
            raise ValueError('Processing end date must be after start date')
        return v

    @field_validator('final_product_quantity')
    def validate_final_product_quantity(cls, v, values):
        if v and values.get('target_quantity') and v > values['target_quantity'] * 1.1:
            raise ValueError('Final product quantity cannot exceed target quantity by more than 10%')
        return v

    @field_validator('production_date')
    def validate_production_date(cls, v):
        if v and v > datetime.now():
            raise ValueError('Production date cannot be in the future')
        return v

    @field_validator('target_quantity')
    def validate_target_quantity(cls, v):
        if v <= 0:
            raise ValueError('Target quantity must be greater than 0')
        return v

    @field_validator('recipe_id')
    def validate_recipe_id(cls, v):
        if v and v <= 0:
            raise ValueError('Recipe ID must be greater than 0')
        return v

    @field_validator('ingredients')
    def validate_ingredients(cls, v):
        if not v:
            raise ValueError('Ingredients list cannot be empty')
        return v 