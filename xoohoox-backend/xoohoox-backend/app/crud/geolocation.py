from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
import math
import uuid

from app.crud.base import CRUDBase
from app.models.geolocation import Farm, Paddock, Geofence, Harvest, LocationTracking
from app.schemas.geolocation import (
    FarmCreate, FarmUpdate,
    PaddockCreate, PaddockUpdate,
    GeofenceCreate, GeofenceUpdate,
    HarvestCreate, HarvestUpdate,
    LocationTrackingCreate, LocationTrackingUpdate
)


class CRUDFarm(CRUDBase[Farm, FarmCreate, FarmUpdate]):
    def get_by_farm_id(self, db: Session, *, farm_id: str) -> Optional[Farm]:
        return db.query(Farm).filter(Farm.farm_id == farm_id).first()
    
    def get_by_region(self, db: Session, *, region: str) -> List[Farm]:
        return db.query(Farm).filter(Farm.region == region).all()
    
    def get_farm_summary(self, db: Session, *, farm_id: str) -> Optional[Dict[str, Any]]:
        farm = self.get_by_farm_id(db, farm_id=farm_id)
        if not farm:
            return None
        
        # Count active harvests
        active_harvests = db.query(Harvest).filter(
            and_(
                Harvest.farm_id == farm_id,
                Harvest.sample_collected == True
            )
        ).count()
        
        # Count total samples collected
        total_samples = db.query(Harvest).filter(
            and_(
                Harvest.farm_id == farm_id,
                Harvest.sample_collected == True
            )
        ).count()
        
        return {
            "farm_id": farm.farm_id,
            "name": farm.name,
            "region": farm.region,
            "total_paddocks": farm.total_paddocks,
            "total_area_hectares": farm.total_area_hectares,
            "active_harvests": active_harvests,
            "total_samples_collected": total_samples,
            "last_sample_collection": farm.last_sample_collection
        }


class CRUDPaddock(CRUDBase[Paddock, PaddockCreate, PaddockUpdate]):
    def get_by_paddock_id(self, db: Session, *, paddock_id: str) -> Optional[Paddock]:
        return db.query(Paddock).filter(Paddock.paddock_id == paddock_id).first()
    
    def get_by_farm_id(self, db: Session, *, farm_id: str) -> List[Paddock]:
        return db.query(Paddock).filter(Paddock.farm_id == farm_id).all()
    
    def get_by_fruit_type(self, db: Session, *, fruit_type: str) -> List[Paddock]:
        return db.query(Paddock).filter(Paddock.fruit_type == fruit_type).all()
    
    def get_active_paddocks(self, db: Session) -> List[Paddock]:
        return db.query(Paddock).filter(Paddock.status == "Active").all()


class CRUDGeofence(CRUDBase[Geofence, GeofenceCreate, GeofenceUpdate]):
    def get_by_geofence_id(self, db: Session, *, geofence_id: str) -> Optional[Geofence]:
        return db.query(Geofence).filter(Geofence.geofence_id == geofence_id).first()
    
    def get_by_farm_id(self, db: Session, *, farm_id: str) -> List[Geofence]:
        return db.query(Geofence).filter(Geofence.farm_id == farm_id).all()
    
    def get_by_type(self, db: Session, *, geofence_type: str) -> List[Geofence]:
        return db.query(Geofence).filter(Geofence.type == geofence_type).all()
    
    def get_active_geofences(self, db: Session) -> List[Geofence]:
        return db.query(Geofence).filter(Geofence.status == "active").all()
    
    def check_point_in_geofence(self, db: Session, *, latitude: float, longitude: float, geofence_id: str) -> bool:
        """Check if a point is inside a geofence using ray casting algorithm"""
        geofence = self.get_by_geofence_id(db, geofence_id=geofence_id)
        if not geofence or not geofence.coordinates:
            return False
        
        # Ray casting algorithm for point-in-polygon
        point = (latitude, longitude)
        polygon = geofence.coordinates
        
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if longitude > min(p1y, p2y):
                if longitude <= max(p1y, p2y):
                    if latitude <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (longitude - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or latitude <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def get_geofences_near_point(self, db: Session, *, latitude: float, longitude: float, radius_km: float = 10) -> List[Geofence]:
        """Get geofences within a certain radius of a point"""
        geofences = self.get_active_geofences(db)
        nearby_geofences = []
        
        for geofence in geofences:
            if geofence.coordinates:
                # Calculate distance to geofence center (simplified)
                center_lat = sum(coord[0] for coord in geofence.coordinates) / len(geofence.coordinates)
                center_lng = sum(coord[1] for coord in geofence.coordinates) / len(geofence.coordinates)
                
                distance = self.calculate_distance(latitude, longitude, center_lat, center_lng)
                if distance <= radius_km:
                    nearby_geofences.append(geofence)
        
        return nearby_geofences


class CRUDHarvest(CRUDBase[Harvest, HarvestCreate, HarvestUpdate]):
    def get_by_harvest_id(self, db: Session, *, harvest_id: str) -> Optional[Harvest]:
        return db.query(Harvest).filter(Harvest.harvest_id == harvest_id).first()
    
    def get_by_batch_id(self, db: Session, *, batch_id: str) -> Optional[Harvest]:
        return db.query(Harvest).filter(Harvest.batch_id == batch_id).first()
    
    def get_by_farm_id(self, db: Session, *, farm_id: str) -> List[Harvest]:
        return db.query(Harvest).filter(Harvest.farm_id == farm_id).all()
    
    def get_by_paddock_id(self, db: Session, *, paddock_id: str) -> List[Harvest]:
        return db.query(Harvest).filter(Harvest.paddock_id == paddock_id).all()
    
    def get_recent_harvests(self, db: Session, *, days: int = 30) -> List[Harvest]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(Harvest).filter(Harvest.harvest_date >= cutoff_date).all()
    
    def get_samples_collected(self, db: Session) -> List[Harvest]:
        return db.query(Harvest).filter(Harvest.sample_collected == True).all()
    
    def get_by_fruit_type(self, db: Session, *, fruit_type: str) -> List[Harvest]:
        return db.query(Harvest).filter(Harvest.fruit_type == fruit_type).all()


class CRUDLocationTracking(CRUDBase[LocationTracking, LocationTrackingCreate, LocationTrackingUpdate]):
    def get_by_tracking_id(self, db: Session, *, tracking_id: str) -> Optional[LocationTracking]:
        return db.query(LocationTracking).filter(LocationTracking.tracking_id == tracking_id).first()
    
    def get_by_batch_id(self, db: Session, *, batch_id: str) -> List[LocationTracking]:
        return db.query(LocationTracking).filter(LocationTracking.batch_id == batch_id).order_by(LocationTracking.timestamp).all()
    
    def get_by_harvest_id(self, db: Session, *, harvest_id: str) -> List[LocationTracking]:
        return db.query(LocationTracking).filter(LocationTracking.harvest_id == harvest_id).order_by(LocationTracking.timestamp).all()
    
    def get_recent_tracking(self, db: Session, *, hours: int = 24) -> List[LocationTracking]:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return db.query(LocationTracking).filter(LocationTracking.timestamp >= cutoff_time).all()
    
    def get_current_location(self, db: Session, *, batch_id: str) -> Optional[LocationTracking]:
        """Get the most recent location for a batch"""
        return db.query(LocationTracking).filter(
            LocationTracking.batch_id == batch_id
        ).order_by(LocationTracking.timestamp.desc()).first()
    
    def create_tracking_entry(self, db: Session, *, batch_id: str, harvest_id: str, latitude: float, longitude: float, 
                            location_name: str = None, status: str = None, source: str = "GPS") -> LocationTracking:
        """Create a new tracking entry"""
        tracking_data = LocationTrackingCreate(
            tracking_id=f"TRACK_{uuid.uuid4().hex[:8].upper()}",
            batch_id=batch_id,
            harvest_id=harvest_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.utcnow(),
            location_name=location_name,
            status=status,
            source=source
        )
        return self.create(db, obj_in=tracking_data)
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def get_route_history(self, db: Session, *, batch_id: str) -> List[Dict[str, Any]]:
        """Get complete route history for a batch"""
        tracking_entries = self.get_by_batch_id(db, batch_id=batch_id)
        route_history = []
        
        for entry in tracking_entries:
            route_history.append({
                "timestamp": entry.timestamp,
                "latitude": entry.latitude,
                "longitude": entry.longitude,
                "location_name": entry.location_name,
                "status": entry.status,
                "source": entry.source
            })
        
        return route_history


# Create CRUD instances
farm = CRUDFarm(Farm)
paddock = CRUDPaddock(Paddock)
geofence = CRUDGeofence(Geofence)
harvest = CRUDHarvest(Harvest)
location_tracking = CRUDLocationTracking(LocationTracking)

