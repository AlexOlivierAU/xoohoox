from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class JuicingLog(Base):
    __tablename__ = "juicing_logs"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, ForeignKey("batches.batch_id"), index=True)
    juice_type = Column(String)
    juicing_date = Column(DateTime, default=datetime.utcnow)
    yield_liters = Column(Float)
    sediment_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = relationship("Batch", back_populates="juicing_logs") 