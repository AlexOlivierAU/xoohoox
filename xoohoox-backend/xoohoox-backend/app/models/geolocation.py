from sqlalchemy import Column, String, Float, DateTime, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.db.base_class import Base


class Farm(Base):
    """Farm model for storing farm information with geolocation"""
    __tablename__ = "farms"

    id = Column(String, primary_key=True, index=True)
    farm_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    farmer_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    region = Column(String, nullable=True)
    total_paddocks = Column(Integer, default=0)
    total_area_hectares = Column(Float, default=0.0)
    established = Column(String, nullable=True)
    certification = Column(String, nullable=True)
    last_sample_collection = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    paddocks = relationship("Paddock", back_populates="farm", cascade="all, delete-orphan")
    geofences = relationship("Geofence", back_populates="farm", cascade="all, delete-orphan")
    harvests = relationship("Harvest", back_populates="farm", cascade="all, delete-orphan")


class Paddock(Base):
    """Paddock model for storing paddock information"""
    __tablename__ = "paddocks"

    id = Column(String, primary_key=True, index=True)
    paddock_id = Column(String, unique=True, index=True, nullable=False)
    farm_id = Column(String, ForeignKey("farms.farm_id"), nullable=False)
    name = Column(String, nullable=False)
    fruit_type = Column(String, nullable=False)
    area_hectares = Column(Float, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    planting_date = Column(DateTime, nullable=True)
    last_harvest = Column(DateTime, nullable=True)
    yield_kg = Column(Float, default=0.0)
    soil_type = Column(String, nullable=True)
    irrigation = Column(String, nullable=True)
    status = Column(String, default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farm = relationship("Farm", back_populates="paddocks")
    harvests = relationship("Harvest", back_populates="paddock", cascade="all, delete-orphan")


class Geofence(Base):
    """Geofence model for storing geofence information"""
    __tablename__ = "geofences"

    id = Column(String, primary_key=True, index=True)
    geofence_id = Column(String, unique=True, index=True, nullable=False)
    farm_id = Column(String, ForeignKey("farms.farm_id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # archive, processing, quality, etc.
    coordinates = Column(JSONB, nullable=True)  # Store as array of [lat, lng] pairs
    radius_meters = Column(Float, default=0.0)
    status = Column(String, default="active")
    alerts_enabled = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farm = relationship("Farm", back_populates="geofences")


class Harvest(Base):
    """Harvest model for storing harvest information"""
    __tablename__ = "harvests"

    id = Column(String, primary_key=True, index=True)
    harvest_id = Column(String, unique=True, index=True, nullable=False)
    paddock_id = Column(String, ForeignKey("paddocks.paddock_id"), nullable=False)
    farm_id = Column(String, ForeignKey("farms.farm_id"), nullable=False)
    batch_id = Column(String, nullable=False)
    fruit_type = Column(String, nullable=False)
    harvest_date = Column(DateTime, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    harvest_method = Column(String, nullable=True)  # mechanical, manual
    weather_conditions = Column(String, nullable=True)
    quality_score = Column(Float, default=0.0)
    sample_collected = Column(Boolean, default=False)
    sample_id = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    paddock = relationship("Paddock", back_populates="harvests")
    farm = relationship("Farm", back_populates="harvests")
    location_tracking = relationship("LocationTracking", back_populates="harvest", cascade="all, delete-orphan")


class LocationTracking(Base):
    """Location tracking model for storing GPS tracking data"""
    __tablename__ = "location_tracking"

    id = Column(String, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True, nullable=False)
    batch_id = Column(String, nullable=False)
    harvest_id = Column(String, ForeignKey("harvests.harvest_id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    location_name = Column(String, nullable=True)
    status = Column(String, nullable=True)  # Sample collected, In transit, Delivered, etc.
    source = Column(String, default="GPS")  # GPS, Manual, etc.
    geofence_id = Column(String, ForeignKey("geofences.geofence_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    harvest = relationship("Harvest", back_populates="location_tracking")
    geofence = relationship("Geofence")

