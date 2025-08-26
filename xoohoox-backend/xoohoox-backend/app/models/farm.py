from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String, unique=True, index=True)
    field_name = Column(String)
    crop_type = Column(String)
    soil_notes = Column(Text)
    weather_notes = Column(Text)
    season = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # batches = relationship("Batch", back_populates="farm")  # Commented out - no foreign key 