from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, ForeignKey("batches.batch_id"), index=True)
    score_aroma = Column(Float)
    score_color = Column(Float)
    score_taste = Column(Float)
    evaluator_name = Column(String)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = relationship("Batch", back_populates="evaluations") 