#!/usr/bin/env python3
"""
Create maintenance-related tables for XooHooX backend - Isolated version
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text, text
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Create a new Base for this script
Base = declarative_base()

class Equipment(Base):
    """Model for equipment in the juice production facility"""
    __tablename__ = "equipment"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default='operational', server_default='operational')
    capacity = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    manufacturer = Column(String(100), nullable=True)
    model_number = Column(String(50), nullable=True)
    serial_number = Column(String(50), nullable=True)
    installation_date = Column(DateTime, nullable=True)
    last_maintenance_date = Column(DateTime, nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    is_critical = Column(Boolean, default=False, nullable=False)
    location = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class MaintenanceLog(Base):
    """Model for logging maintenance activities"""
    __tablename__ = "maintenance_log"
    __table_args__ = {'schema': 'public'}
    
    id = Column(Integer, primary_key=True, index=True)
    maintenance_id = Column(Integer, ForeignKey("public.equipment_maintenance.id"), nullable=False)
    log_date = Column(DateTime, nullable=False)
    log_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    performed_by = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class EquipmentMaintenance(Base):
    """Model for tracking equipment maintenance and repairs"""
    __tablename__ = "equipment_maintenance"
    __table_args__ = {'schema': 'public'}
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("public.equipment.id"), nullable=False)
    equipment_type = Column(String(50), nullable=False)
    maintenance_type = Column(String(50), nullable=False)
    maintenance_status = Column(String(50), nullable=False)
    maintenance_date = Column(DateTime, nullable=False)
    next_maintenance_date = Column(DateTime, nullable=True)
    cost = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    work_performed = Column(Text, nullable=True)
    technician = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

def create_maintenance_tables():
    """Create only the maintenance-related tables"""
    print("Creating maintenance tables...")
    
    # Create database engine
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        pool_recycle=300
    )
    
    # Set schema and create tables
    with engine.connect() as conn:
        conn.execute(text('SET search_path TO public'))
        conn.commit()
        Base.metadata.create_all(bind=engine)
    
    print("Maintenance tables created successfully!")

if __name__ == "__main__":
    create_maintenance_tables()
