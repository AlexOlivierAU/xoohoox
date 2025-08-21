from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class FermentationLog(Base):
    __tablename__ = "fermentation_logs"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, ForeignKey("batches.batch_id"), index=True)
    day_number = Column(Integer)
    temperature = Column(Float)
    ph_level = Column(Float)
    sg_reading = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = relationship("Batch", back_populates="fermentation_logs") 