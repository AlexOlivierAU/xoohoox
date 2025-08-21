from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class PathTaken(str, enum.Enum):
    VINEGAR = "vinegar"
    DISTILLATION = "distillation"
    ARCHIVED = "archived"

class JuiceVariant(str, enum.Enum):
    JP1 = "JP1"
    JP2 = "JP2"
    JP3 = "JP3"
    JP4 = "JP4"
    JP5 = "JP5"

class FermentationTrial(Base):
    __tablename__ = "fermentation_trials"

    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(String, unique=True, index=True)  # e.g., T-042-03
    batch_id = Column(Integer, ForeignKey("batches.id"))
    
    # Trial Parameters
    yeast_strain = Column(String)
    juice_variant = Column(Enum(JuiceVariant))
    initial_volume = Column(Float)
    
    # Measurements
    sg = Column(Float)  # Specific Gravity
    ph = Column(Float)
    brix = Column(Float)
    current_abv = Column(Float)
    
    # Status and Path
    path_taken = Column(Enum(PathTaken), nullable=True)
    status = Column(String)  # Fermenting, Awaiting, Complete, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # JSON Fields for Complex Data
    daily_readings = Column(JSON, default=list)  # List of daily measurement records
    upscale_history = Column(JSON, default=list)  # List of upscale events
    compound_results = Column(JSON, default=dict)  # Compound test results
    
    # Relationships
    batch = relationship("Batch", back_populates="trials")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.trial_id and self.batch_id:
            # Generate trial_id based on batch and sequence
            # Format: T-042-03 (Trial 3 of Batch 42)
            pass  # TODO: Implement trial_id generation logic

    def record_daily_reading(self, sg: float, ph: float, brix: float, abv: float, notes: str = None):
        """Record a new daily reading."""
        reading = {
            "timestamp": datetime.utcnow().isoformat(),
            "sg": sg,
            "ph": ph,
            "brix": brix,
            "abv": abv,
            "notes": notes
        }
        if not isinstance(self.daily_readings, list):
            self.daily_readings = []
        self.daily_readings.append(reading)
        self.current_abv = abv
        
        # Check if ABV threshold is reached
        if abv > 8.0 and self.path_taken is None:
            self.status = "Ready for Branching"

    def record_upscale(self, test_number: int, volume: float, notes: str = None):
        """Record an upscale event."""
        upscale = {
            "timestamp": datetime.utcnow().isoformat(),
            "test_number": test_number,
            "volume": volume,
            "notes": notes
        }
        if not isinstance(self.upscale_history, list):
            self.upscale_history = []
        self.upscale_history.append(upscale)

    def set_path(self, path: PathTaken):
        """Set the path taken for this trial."""
        self.path_taken = path
        self.status = f"{path.value.title()} Path" 