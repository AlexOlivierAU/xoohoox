from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)
    maintenance_id = Column(Integer, ForeignKey("maintenances.id"), nullable=False)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_taken = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    parts_replaced = Column(String, nullable=True)
    cost = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    maintenance = relationship("Maintenance", back_populates="logs")
    technician = relationship("User", back_populates="maintenance_logs") 