from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class YeastStrain(Base):
    __tablename__ = "yeast_strains"

    id = Column(Integer, primary_key=True, index=True)
    strain_name = Column(String, unique=True, index=True)
    genetic_notes = Column(Text)
    function_tags = Column(JSON)  # Store as JSON array
    origin = Column(String)
    last_tested_batch = Column(String, ForeignKey("batches.batch_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = relationship("Batch", back_populates="yeast_strain") 