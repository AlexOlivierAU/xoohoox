from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class UpscaleStage(str, enum.Enum):
    TEST_4 = "Test 4"
    TEST_5 = "Test 5"
    TEST_6 = "Test 6"

class UpscaleStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"

class UpscaleRun(Base):
    __tablename__ = "upscale_runs"

    id = Column(Integer, primary_key=True, index=True)
    upscale_id = Column(String, unique=True, index=True)  # U-042-03-5L format
    trial_id = Column(Integer, ForeignKey("fermentation_trials.id"))
    stage = Column(Enum(UpscaleStage))
    volume = Column(Float)  # in Liters
    yield_amount = Column(Float)  # in mL or L
    abv_result = Column(Float)
    compound_summary = Column(String, nullable=True)
    status = Column(Enum(UpscaleStatus), default=UpscaleStatus.PENDING)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trial = relationship("FermentationTrial", back_populates="upscale_runs")

    def __repr__(self):
        return f"<UpscaleRun {self.upscale_id}>" 