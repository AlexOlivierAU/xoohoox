from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import FruitType, ProcessStatus

class BatchTracking(Base):
    __tablename__ = "batch_tracking"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    fruit_type = Column(SQLEnum(FruitType), nullable=False)
    process_type = Column(String, nullable=False)
    grower_id = Column(String, nullable=True)
    status = Column(String, nullable=False, default="planned")
    stage = Column(String, nullable=False, default="initial")
    progress = Column(Float, nullable=False, default=0.0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Additional metadata
    quality_checks = Column(JSON, nullable=True, default=list)
    maintenance_records = Column(JSON, nullable=True, default=list)
    environmental_impact = Column(JSON, nullable=True)
    processing_start_date = Column(DateTime, nullable=True)
    processing_end_date = Column(DateTime, nullable=True)
    final_product_quantity = Column(Float, nullable=True)
    production_date = Column(DateTime, nullable=True)
    recipe_id = Column(Integer, nullable=True)
    ingredients = Column(JSON, nullable=True, default=list)

    def __repr__(self):
        return f"<Batch {self.batch_id} ({self.name})>" 