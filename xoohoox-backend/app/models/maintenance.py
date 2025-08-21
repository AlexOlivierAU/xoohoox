from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Maintenance(Base):
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    maintenance_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    completion_date = Column(DateTime, nullable=True)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)
    performed_by = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")
    maintenance_logs = relationship("MaintenanceLog", back_populates="maintenance")

    def __repr__(self):
        return f"<Maintenance(id={self.id}, equipment_id={self.equipment_id}, type={self.maintenance_type})>" 