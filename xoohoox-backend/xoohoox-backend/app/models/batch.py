from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import BatchStatus, FruitType, JuiceType

class Batch(BaseModel):
    __tablename__ = "batches"
    name = Column(String, index=True)
    fruit_type = Column(Enum(FruitType), nullable=False)
    juice_type = Column(Enum(JuiceType), nullable=False)
    status = Column(Enum(BatchStatus), default=BatchStatus.PLANNED)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    target_volume = Column(Float, nullable=False)
    actual_volume = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    batch_metadata = Column(JSON, nullable=True)
    
    # Relationships
    # farm = relationship("Farm", back_populates="batch")  # Commented out - no foreign key
    juicing_logs = relationship("JuicingLog", back_populates="batch")
    fermentation_logs = relationship("FermentationLog", back_populates="batch")
    evaluations = relationship("Evaluation", back_populates="batch")
    yeast_strain = relationship("YeastStrain", back_populates="batch")
    trials = relationship("FermentationTrial", back_populates="batch")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate()

    def validate(self):
        if self.target_volume <= 0:
            raise ValueError("Target volume must be positive")
        if self.actual_volume is not None and self.actual_volume < 0:
            raise ValueError("Actual volume cannot be negative")
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date") 