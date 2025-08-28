from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from app.api import deps
from app.schemas.geolocation import (
    Farm, FarmCreate, FarmUpdate, FarmWithDetails, FarmSummary,
    Paddock, PaddockCreate, PaddockUpdate, PaddockWithDetails,
    Geofence, GeofenceCreate, GeofenceUpdate,
    Harvest, HarvestCreate, HarvestUpdate, HarvestWithDetails,
    LocationTracking, LocationTrackingCreate, LocationTrackingUpdate,
    GeofenceAlert, SampleTracking
)

router = APIRouter()

# Mock data storage (in production, this would be in a database)
MOCK_FARMS = [
    {
        "id": "farm_001",
        "farm_id": "FARM_001",
        "name": "Sunshine Citrus Farms",
        "farmer_name": "John Smith",
        "phone": "(03) 5023 1234",
        "email": "john@sunshinecitrus.com.au",
        "latitude": -34.2860,
        "longitude": 142.2630,
        "address": "123 Citrus Grove Rd, Mildura VIC 3500",
        "region": "Victoria",
        "total_paddocks": 8,
        "total_area_hectares": 120,
        "established": "2015",
        "certification": "Organic",
        "last_sample_collection": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "farm_002",
        "farm_id": "FARM_002",
        "name": "Golden Apple Orchards",
        "farmer_name": "Sarah Johnson",
        "phone": "(03) 6234 5678",
        "email": "sarah@goldenapple.com.au",
        "latitude": -43.0826,
        "longitude": 147.1277,
        "address": "456 Apple Valley Dr, Hobart TAS 7000",
        "region": "Tasmania",
        "total_paddocks": 12,
        "total_area_hectares": 85,
        "established": "2018",
        "certification": "HACCP",
        "last_sample_collection": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "farm_003",
        "farm_id": "FARM_003",
        "name": "Tropical Fruit Paradise",
        "farmer_name": "Mike Wilson",
        "phone": "(07) 4031 2345",
        "email": "mike@tropicalfruit.com.au",
        "latitude": -17.1191,
        "longitude": 145.6786,
        "address": "789 Mango Lane, Cairns QLD 4870",
        "region": "Queensland",
        "total_paddocks": 6,
        "total_area_hectares": 65,
        "established": "2020",
        "certification": "GAP",
        "last_sample_collection": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

MOCK_PADDOCKS = [
    {
        "id": "paddock_001",
        "paddock_id": "PADDOCK_001",
        "farm_id": "FARM_001",
        "name": "Orange Grove A",
        "fruit_type": "Orange",
        "area_hectares": 15,
        "latitude": -34.2860,
        "longitude": 142.2630,
        "planting_date": "2015-03-15T00:00:00",
        "last_harvest": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        "yield_kg": 2500,
        "soil_type": "Sandy Loam",
        "irrigation": "Drip",
        "status": "Active",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "paddock_002",
        "paddock_id": "PADDOCK_002",
        "farm_id": "FARM_001",
        "name": "Lemon Grove B",
        "fruit_type": "Lemon",
        "area_hectares": 12,
        "latitude": -34.2960,
        "longitude": 142.2730,
        "planting_date": "2016-08-20T00:00:00",
        "last_harvest": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "yield_kg": 1800,
        "soil_type": "Clay Loam",
        "irrigation": "Sprinkler",
        "status": "Active",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "paddock_003",
        "paddock_id": "PADDOCK_003",
        "farm_id": "FARM_002",
        "name": "Apple Orchard North",
        "fruit_type": "Apple",
        "area_hectares": 20,
        "latitude": -43.0826,
        "longitude": 147.1277,
        "planting_date": "2018-04-10T00:00:00",
        "last_harvest": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        "yield_kg": 3200,
        "soil_type": "Volcanic",
        "irrigation": "Drip",
        "status": "Active",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

MOCK_GEOFENCES = [
    {
        "id": "geo_001",
        "geofence_id": "GEO_001",
        "farm_id": "FARM_001",
        "name": "Sample Archive Zone",
        "type": "archive",
        "coordinates": [[-34.2860, 142.2630], [-34.2860, 142.2730], [-34.2960, 142.2730], [-34.2960, 142.2630]],
        "radius_meters": 500,
        "status": "active",
        "alerts_enabled": True,
        "description": "Laboratory sample archive storage area",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "geo_002",
        "geofence_id": "GEO_002",
        "farm_id": "FARM_002",
        "name": "Laboratory Processing Zone",
        "type": "processing",
        "coordinates": [[-43.0826, 147.1277], [-43.0826, 147.1377], [-43.0926, 147.1377], [-43.0926, 147.1277]],
        "radius_meters": 300,
        "status": "active",
        "alerts_enabled": True,
        "description": "Sample processing and analysis area",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

MOCK_HARVESTS = [
    {
        "id": "harvest_001",
        "harvest_id": "HARVEST_001",
        "paddock_id": "PADDOCK_001",
        "farm_id": "FARM_001",
        "batch_id": "BATCH_001",
        "fruit_type": "Orange",
        "harvest_date": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        "quantity_kg": 2500,
        "harvest_method": "mechanical",
        "weather_conditions": "Sunny, 25°C",
        "quality_score": 8.5,
        "sample_collected": True,
        "sample_id": "SAMPLE_001",
        "notes": "Excellent quality oranges, ready for laboratory analysis",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "harvest_002",
        "harvest_id": "HARVEST_002",
        "paddock_id": "PADDOCK_002",
        "farm_id": "FARM_001",
        "batch_id": "BATCH_002",
        "fruit_type": "Lemon",
        "harvest_date": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "quantity_kg": 1800,
        "harvest_method": "manual",
        "weather_conditions": "Partly cloudy, 22°C",
        "quality_score": 8.2,
        "sample_collected": True,
        "sample_id": "SAMPLE_002",
        "notes": "Good quality lemons, suitable for research samples",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": "harvest_003",
        "harvest_id": "HARVEST_003",
        "paddock_id": "PADDOCK_003",
        "farm_id": "FARM_002",
        "batch_id": "BATCH_003",
        "fruit_type": "Apple",
        "harvest_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        "quantity_kg": 3200,
        "harvest_method": "mechanical",
        "weather_conditions": "Rainy, 18°C",
        "quality_score": 7.8,
        "sample_collected": True,
        "sample_id": "SAMPLE_003",
        "notes": "Apples collected in wet conditions, extra care needed",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

MOCK_LOCATION_TRACKING = [
    {
        "id": "track_001",
        "tracking_id": "TRACK_001",
        "batch_id": "BATCH_001",
        "harvest_id": "HARVEST_001",
        "latitude": -34.2860,
        "longitude": 142.2630,
        "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        "location_name": "Mildura Farm",
        "status": "Sample collected",
        "source": "GPS",
        "geofence_id": "GEO_001",
        "created_at": datetime.utcnow().isoformat()
    },
    {
        "id": "track_002",
        "tracking_id": "TRACK_002",
        "batch_id": "BATCH_001",
        "harvest_id": "HARVEST_001",
        "latitude": -36.7578,
        "longitude": 144.2789,
        "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
        "location_name": "Bendigo Transit",
        "status": "In transit to laboratory",
        "source": "GPS",
        "geofence_id": None,
        "created_at": datetime.utcnow().isoformat()
    },
    {
        "id": "track_003",
        "tracking_id": "TRACK_003",
        "batch_id": "BATCH_001",
        "harvest_id": "HARVEST_001",
        "latitude": -37.8136,
        "longitude": 144.9631,
        "timestamp": datetime.utcnow().isoformat(),
        "location_name": "Melbourne Laboratory",
        "status": "Delivered to laboratory",
        "source": "GPS",
        "geofence_id": "GEO_002",
        "created_at": datetime.utcnow().isoformat()
    }
]

@router.get("/farms/", response_model=List[Farm])
def read_farms(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    region: Optional[str] = Query(None, description="Filter by region")
):
    """Retrieve farms with optional region filtering"""
    farms = MOCK_FARMS[skip:skip + limit]
    if region:
        farms = [farm for farm in farms if farm.get("region") == region]
    return farms

@router.get("/farms/{farm_id}", response_model=Farm)
def read_farm(farm_id: str, db: Session = Depends(deps.get_db)):
    """Get a specific farm by ID"""
    farm = next((farm for farm in MOCK_FARMS if farm["farm_id"] == farm_id), None)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@router.get("/paddocks/", response_model=List[Paddock])
def read_paddocks(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    farm_id: Optional[str] = Query(None, description="Filter by farm ID")
):
    """Retrieve paddocks with optional farm filtering"""
    paddocks = MOCK_PADDOCKS[skip:skip + limit]
    if farm_id:
        paddocks = [paddock for paddock in paddocks if paddock.get("farm_id") == farm_id]
    return paddocks

@router.get("/paddocks/{paddock_id}", response_model=Paddock)
def read_paddock(paddock_id: str, db: Session = Depends(deps.get_db)):
    """Get a specific paddock by ID"""
    paddock = next((paddock for paddock in MOCK_PADDOCKS if paddock["paddock_id"] == paddock_id), None)
    if not paddock:
        raise HTTPException(status_code=404, detail="Paddock not found")
    return paddock

@router.get("/geofences/", response_model=List[Geofence])
def read_geofences(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    farm_id: Optional[str] = Query(None, description="Filter by farm ID"),
    type: Optional[str] = Query(None, description="Filter by geofence type")
):
    """Retrieve geofences with optional filtering"""
    geofences = MOCK_GEOFENCES[skip:skip + limit]
    if farm_id:
        geofences = [geo for geo in geofences if geo.get("farm_id") == farm_id]
    if type:
        geofences = [geo for geo in geofences if geo.get("type") == type]
    return geofences

@router.get("/geofences/{geofence_id}", response_model=Geofence)
def read_geofence(geofence_id: str, db: Session = Depends(deps.get_db)):
    """Get a specific geofence by ID"""
    geofence = next((geo for geo in MOCK_GEOFENCES if geo["geofence_id"] == geofence_id), None)
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    return geofence

@router.get("/harvests/", response_model=List[Harvest])
def read_harvests(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    farm_id: Optional[str] = Query(None, description="Filter by farm ID"),
    batch_id: Optional[str] = Query(None, description="Filter by batch ID")
):
    """Retrieve harvests with optional filtering"""
    harvests = MOCK_HARVESTS[skip:skip + limit]
    if farm_id:
        harvests = [harvest for harvest in harvests if harvest.get("farm_id") == farm_id]
    if batch_id:
        harvests = [harvest for harvest in harvests if harvest.get("batch_id") == batch_id]
    return harvests

@router.get("/harvests/{harvest_id}", response_model=Harvest)
def read_harvest(harvest_id: str, db: Session = Depends(deps.get_db)):
    """Get a specific harvest by ID"""
    harvest = next((harvest for harvest in MOCK_HARVESTS if harvest["harvest_id"] == harvest_id), None)
    if not harvest:
        raise HTTPException(status_code=404, detail="Harvest not found")
    return harvest

@router.get("/location-tracking/", response_model=List[LocationTracking])
def read_location_tracking(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    batch_id: Optional[str] = Query(None, description="Filter by batch ID"),
    harvest_id: Optional[str] = Query(None, description="Filter by harvest ID")
):
    """Retrieve location tracking data with optional filtering"""
    tracking = MOCK_LOCATION_TRACKING[skip:skip + limit]
    if batch_id:
        tracking = [track for track in tracking if track.get("batch_id") == batch_id]
    if harvest_id:
        tracking = [track for track in tracking if track.get("harvest_id") == harvest_id]
    return tracking

@router.get("/location-tracking/{tracking_id}", response_model=LocationTracking)
def read_location_tracking_item(tracking_id: str, db: Session = Depends(deps.get_db)):
    """Get a specific location tracking record by ID"""
    tracking = next((track for track in MOCK_LOCATION_TRACKING if track["tracking_id"] == tracking_id), None)
    if not tracking:
        raise HTTPException(status_code=404, detail="Location tracking record not found")
    return tracking

@router.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(deps.get_db)):
    """Get dashboard summary statistics"""
    total_farms = len(MOCK_FARMS)
    total_paddocks = len(MOCK_PADDOCKS)
    total_harvests = len(MOCK_HARVESTS)
    active_geofences = len([geo for geo in MOCK_GEOFENCES if geo.get("status") == "active"])
    
    recent_harvests = sorted(MOCK_HARVESTS, key=lambda x: x.get("harvest_date", ""), reverse=True)[:5]
    
    return {
        "total_farms": total_farms,
        "total_paddocks": total_paddocks,
        "total_harvests": total_harvests,
        "active_geofences": active_geofences,
        "recent_harvests": recent_harvests
    }

@router.get("/geofences/{geofence_id}/check-point")
def check_point_in_geofence(
    geofence_id: str,
    latitude: float = Query(..., description="Point latitude"),
    longitude: float = Query(..., description="Point longitude"),
    db: Session = Depends(deps.get_db)
):
    """Check if a point is inside a geofence"""
    geofence = next((geo for geo in MOCK_GEOFENCES if geo["geofence_id"] == geofence_id), None)
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    # Simple point-in-polygon check (ray casting algorithm)
    coordinates = geofence.get("coordinates", [])
    if not coordinates:
        return {"inside": False, "message": "No coordinates defined for geofence"}
    
    # Ray casting algorithm
    n = len(coordinates)
    inside = False
    
    p1x, p1y = coordinates[0]
    for i in range(n + 1):
        p2x, p2y = coordinates[i % n]
        if longitude > min(p1y, p2y):
            if longitude <= max(p1y, p2y):
                if latitude <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (longitude - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or latitude <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return {
        "inside": inside,
        "geofence_id": geofence_id,
        "point": {"latitude": latitude, "longitude": longitude},
        "geofence_name": geofence.get("name")
    }
