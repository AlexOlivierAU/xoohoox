from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class YeastStrain(BaseModel):
    __tablename__ = "yeast_strains"
    strain_name = Column(String, unique=True, index=True)
    genetic_notes = Column(Text)
    function_tags = Column(JSON)  # Store as JSON array
    origin = Column(String)
    last_tested_batch = Column(Integer, ForeignKey("batches.id"), nullable=True)
    
    # Relationships
    batch = relationship("Batch", back_populates="yeast_strain") 