from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class JuicingLog(BaseModel):
    __tablename__ = "juicing_logs"
    batch_id = Column(Integer, ForeignKey("batches.id"), index=True)
    juice_type = Column(String)
    juicing_date = Column(DateTime, default=datetime.utcnow)
    yield_liters = Column(Float)
    sediment_notes = Column(Text)
    
    # Relationships
    batch = relationship("Batch", back_populates="juicing_logs") 