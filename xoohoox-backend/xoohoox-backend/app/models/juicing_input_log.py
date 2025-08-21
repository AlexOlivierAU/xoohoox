from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import ProcessStatus

class JuicingInputLog(BaseModel):
    """Model for logging juicing process inputs and parameters"""
    __tablename__ = "juicing_input_log"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(String(10), unique=True, index=True, nullable=False)
    batch_id = Column(String(10), ForeignKey("batch_tracking.batch_id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    operator_id = Column(String(50), nullable=False)
    equipment_id = Column(String(50), nullable=False)
    input_quantity_kg = Column(Float, nullable=False)
    temperature_c = Column(Float, nullable=False)
    pressure_bar = Column(Float, nullable=False)
    duration_minutes = Column(Float, nullable=False)
    output_quantity_l = Column(Float, nullable=False)
    brix_reading = Column(Float, nullable=False)
    ph_level = Column(Float, nullable=False)
    turbidity_ntu = Column(Float, nullable=False)
    process_notes = Column(Text, nullable=True)
    quality_issues = Column(Text, nullable=True)
    process_status = Column(Enum(ProcessStatus), default=ProcessStatus.STARTED, nullable=False)
    
    # Relationships
    batch = relationship("BatchTracking", back_populates="juicing_logs", lazy="joined")
    quality_checks = relationship("QualityControl", back_populates="juicing_input", lazy="joined", foreign_keys="QualityControl.juicing_input_id") 