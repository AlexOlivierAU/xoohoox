from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class GeofenceType(str, Enum):
    ARCHIVE = "archive"
    PROCESSING = "processing"
    QUALITY = "quality"
    STORAGE = "storage"
    TRANSIT = "transit"


class TrackingSource(str, Enum):
    GPS = "GPS"
    MANUAL = "Manual"
    MOBILE_APP = "Mobile App"
    SENSOR = "Sensor"


class HarvestMethod(str, Enum):
    MECHANICAL = "mechanical"
    MANUAL = "manual"
    COMBINED = "combined"


# Base schemas
class FarmBase(BaseModel):
    farm_id: str = Field(..., description="Unique farm identifier")
    name: str = Field(..., description="Farm name")
    farmer_name: str = Field(..., description="Farmer's name")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[str] = Field(None, description="Contact email")
    latitude: Optional[float] = Field(None, description="Farm latitude")
    longitude: Optional[float] = Field(None, description="Farm longitude")
    address: Optional[str] = Field(None, description="Farm address")
    region: Optional[str] = Field(None, description="Australian region")
    total_paddocks: int = Field(0, description="Total number of paddocks")
    total_area_hectares: float = Field(0.0, description="Total farm area in hectares")
    established: Optional[str] = Field(None, description="Year established")
    certification: Optional[str] = Field(None, description="Farm certification")


class PaddockBase(BaseModel):
    paddock_id: str = Field(..., description="Unique paddock identifier")
    farm_id: str = Field(..., description="Associated farm ID")
    name: str = Field(..., description="Paddock name")
    fruit_type: str = Field(..., description="Type of fruit grown")
    area_hectares: float = Field(..., description="Paddock area in hectares")
    latitude: Optional[float] = Field(None, description="Paddock latitude")
    longitude: Optional[float] = Field(None, description="Paddock longitude")
    planting_date: Optional[datetime] = Field(None, description="Date planted")
    last_harvest: Optional[datetime] = Field(None, description="Last harvest date")
    yield_kg: float = Field(0.0, description="Last harvest yield in kg")
    soil_type: Optional[str] = Field(None, description="Soil type")
    irrigation: Optional[str] = Field(None, description="Irrigation method")
    status: str = Field("Active", description="Paddock status")


class GeofenceBase(BaseModel):
    geofence_id: str = Field(..., description="Unique geofence identifier")
    farm_id: str = Field(..., description="Associated farm ID")
    name: str = Field(..., description="Geofence name")
    type: GeofenceType = Field(..., description="Geofence type")
    coordinates: Optional[List[List[float]]] = Field(None, description="Polygon coordinates [[lat, lng]]")
    radius_meters: float = Field(0.0, description="Geofence radius in meters")
    status: str = Field("active", description="Geofence status")
    alerts_enabled: bool = Field(True, description="Whether alerts are enabled")
    description: Optional[str] = Field(None, description="Geofence description")


class HarvestBase(BaseModel):
    harvest_id: str = Field(..., description="Unique harvest identifier")
    paddock_id: str = Field(..., description="Associated paddock ID")
    farm_id: str = Field(..., description="Associated farm ID")
    batch_id: str = Field(..., description="Associated batch ID")
    fruit_type: str = Field(..., description="Type of fruit harvested")
    harvest_date: datetime = Field(..., description="Harvest date")
    quantity_kg: float = Field(..., description="Harvest quantity in kg")
    harvest_method: Optional[HarvestMethod] = Field(None, description="Harvest method")
    weather_conditions: Optional[str] = Field(None, description="Weather during harvest")
    quality_score: float = Field(0.0, description="Quality score (0-10)")
    sample_collected: bool = Field(False, description="Whether sample was collected")
    sample_id: Optional[str] = Field(None, description="Sample identifier")
    notes: Optional[str] = Field(None, description="Harvest notes")


class LocationTrackingBase(BaseModel):
    tracking_id: str = Field(..., description="Unique tracking identifier")
    batch_id: str = Field(..., description="Associated batch ID")
    harvest_id: str = Field(..., description="Associated harvest ID")
    latitude: float = Field(..., description="GPS latitude")
    longitude: float = Field(..., description="GPS longitude")
    timestamp: datetime = Field(..., description="Tracking timestamp")
    location_name: Optional[str] = Field(None, description="Location name")
    status: Optional[str] = Field(None, description="Sample status")
    source: TrackingSource = Field(TrackingSource.GPS, description="Tracking source")
    geofence_id: Optional[str] = Field(None, description="Associated geofence ID")


# Create schemas
class FarmCreate(FarmBase):
    pass


class PaddockCreate(PaddockBase):
    pass


class GeofenceCreate(GeofenceBase):
    pass


class HarvestCreate(HarvestBase):
    pass


class LocationTrackingCreate(LocationTrackingBase):
    pass


# Update schemas
class FarmUpdate(BaseModel):
    name: Optional[str] = None
    farmer_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    region: Optional[str] = None
    total_paddocks: Optional[int] = None
    total_area_hectares: Optional[float] = None
    established: Optional[str] = None
    certification: Optional[str] = None
    last_sample_collection: Optional[datetime] = None


class PaddockUpdate(BaseModel):
    name: Optional[str] = None
    fruit_type: Optional[str] = None
    area_hectares: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    planting_date: Optional[datetime] = None
    last_harvest: Optional[datetime] = None
    yield_kg: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation: Optional[str] = None
    status: Optional[str] = None


class GeofenceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[GeofenceType] = None
    coordinates: Optional[List[List[float]]] = None
    radius_meters: Optional[float] = None
    status: Optional[str] = None
    alerts_enabled: Optional[bool] = None
    description: Optional[str] = None


class HarvestUpdate(BaseModel):
    fruit_type: Optional[str] = None
    harvest_date: Optional[datetime] = None
    quantity_kg: Optional[float] = None
    harvest_method: Optional[HarvestMethod] = None
    weather_conditions: Optional[str] = None
    quality_score: Optional[float] = None
    sample_collected: Optional[bool] = None
    sample_id: Optional[str] = None
    notes: Optional[str] = None


class LocationTrackingUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: Optional[datetime] = None
    location_name: Optional[str] = None
    status: Optional[str] = None
    source: Optional[TrackingSource] = None
    geofence_id: Optional[str] = None


# Response schemas
class Farm(FarmBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Paddock(PaddockBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Geofence(GeofenceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Harvest(HarvestBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationTracking(LocationTrackingBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Extended schemas with relationships
class FarmWithDetails(Farm):
    paddocks: List[Paddock] = []
    geofences: List[Geofence] = []
    harvests: List[Harvest] = []


class PaddockWithDetails(Paddock):
    farm: Farm
    harvests: List[Harvest] = []


class HarvestWithDetails(Harvest):
    paddock: Paddock
    farm: Farm
    location_tracking: List[LocationTracking] = []


# Geolocation-specific schemas
class GeofenceAlert(BaseModel):
    geofence_id: str
    batch_id: str
    alert_type: str  # "enter", "exit"
    timestamp: datetime
    location: Dict[str, float]  # {"latitude": float, "longitude": float}
    message: str


class SampleTracking(BaseModel):
    batch_id: str
    sample_id: str
    current_location: Dict[str, float]
    status: str
    last_update: datetime
    route_history: List[Dict[str, Any]]


class FarmSummary(BaseModel):
    farm_id: str
    name: str
    region: str
    total_paddocks: int
    total_area_hectares: float
    active_harvests: int
    total_samples_collected: int
    last_sample_collection: Optional[datetime]

