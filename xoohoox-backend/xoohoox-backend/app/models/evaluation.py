from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class Evaluation(BaseModel):
    __tablename__ = "evaluations"
    sample_id = Column(Integer, ForeignKey("batches.id"), index=True)
    score_aroma = Column(Float)
    score_color = Column(Float)
    score_taste = Column(Float)
    evaluator_name = Column(String)
    comments = Column(Text)
    
    # Relationships
    batch = relationship("Batch", back_populates="evaluations") 