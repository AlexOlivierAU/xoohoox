from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MaintenanceLog(BaseModel):
    """Model for logging maintenance activities"""
    __tablename__ = "maintenance_log"

    maintenance_id = Column(Integer, ForeignKey("equipment_maintenance.id"), nullable=False)
    log_date = Column(DateTime, nullable=False)
    log_type = Column(String, nullable=False)  # e.g., "Inspection", "Repair", "Service"
    description = Column(String, nullable=False)
    performed_by = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    # Relationship back to EquipmentMaintenance
    maintenance = relationship("EquipmentMaintenance", back_populates="maintenance_logs") 