from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class FermentationLog(BaseModel):
    __tablename__ = "fermentation_logs"
    batch_id = Column(Integer, ForeignKey("batches.id"), index=True)
    day_number = Column(Integer)
    temperature = Column(Float)
    ph_level = Column(Float)
    sg_reading = Column(Float)
    notes = Column(Text)
    
    # Relationships
    batch = relationship("Batch", back_populates="fermentation_logs") 