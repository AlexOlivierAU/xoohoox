from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import MaintenanceType, MaintenanceStatus, EquipmentType

class EquipmentMaintenance(BaseModel):
    """Model for tracking equipment maintenance and repairs"""
    __tablename__ = "equipment_maintenance"

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    equipment_type = Column(Enum(EquipmentType), nullable=False)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    maintenance_status = Column(Enum(MaintenanceStatus), nullable=False)
    maintenance_date = Column(DateTime, nullable=False)
    next_maintenance_date = Column(DateTime, nullable=True)
    cost = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    work_performed = Column(String, nullable=True)
    technician = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")
    maintenance_logs = relationship("MaintenanceLog", back_populates="maintenance") 