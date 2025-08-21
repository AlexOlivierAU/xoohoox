from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ChemistryAdjustment(Base):
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), nullable=False)
    adjustment_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    batch = relationship("Batch", back_populates="chemistry_adjustments")

    def __repr__(self):
        return f"<ChemistryAdjustment(id={self.id}, batch_id={self.batch_id}, type={self.adjustment_type})>" 