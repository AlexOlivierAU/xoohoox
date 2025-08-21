from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class EnvironmentalImpactBase(BaseModel):
    batch_id: int
    water_usage: float = Field(..., description="Water usage in liters")
    energy_consumption: float = Field(..., description="Energy consumption in kWh")
    waste_generated: float = Field(..., description="Waste generated in kg")
    carbon_footprint: float = Field(..., description="Carbon footprint in kg CO2e")
    notes: Optional[str] = None

class EnvironmentalImpactCreate(EnvironmentalImpactBase):
    pass

class EnvironmentalImpactUpdate(EnvironmentalImpactBase):
    batch_id: Optional[int] = None
    water_usage: Optional[float] = None
    energy_consumption: Optional[float] = None
    waste_generated: Optional[float] = None
    carbon_footprint: Optional[float] = None

class EnvironmentalImpactInDB(EnvironmentalImpactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EnvironmentalImpact(EnvironmentalImpactInDB):
    pass 