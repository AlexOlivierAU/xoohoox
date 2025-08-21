from sqlalchemy import Column, String, Float, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import EquipmentType, EquipmentStatus

class Equipment(BaseModel):
    """Model for equipment in the juice production facility"""
    __tablename__ = "equipment"

    name = Column(String(100), nullable=False, index=True)
    type = Column(Enum(EquipmentType), nullable=False)
    status = Column(Enum(EquipmentStatus), nullable=False, default=EquipmentStatus.OPERATIONAL, server_default=EquipmentStatus.OPERATIONAL.value)
    capacity = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    manufacturer = Column(String(100), nullable=True)
    model_number = Column(String(50), nullable=True)
    serial_number = Column(String(50), nullable=True)
    installation_date = Column(DateTime, nullable=True)
    last_maintenance_date = Column(DateTime, nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    is_critical = Column(Boolean, default=False, nullable=False)
    location = Column(String(100), nullable=True)
    notes = Column(String, nullable=True)

    # Relationships
    maintenance_records = relationship("EquipmentMaintenance", back_populates="equipment") 