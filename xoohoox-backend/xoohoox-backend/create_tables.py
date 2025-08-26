#!/usr/bin/env python3
"""
Create maintenance-related tables for XooHooX backend
"""
from app.db.database import engine
from app.models.equipment import Equipment
from app.models.maintenance_log import MaintenanceLog
from app.models.equipment_maintenance import EquipmentMaintenance
from app.models.base import Base
from sqlalchemy import text

def create_maintenance_tables():
    """Create only the maintenance-related tables"""
    print("Creating maintenance tables...")
    
    # Import the models to register them with SQLAlchemy
    # This ensures the tables are included in the metadata
    _ = Equipment
    _ = MaintenanceLog
    _ = EquipmentMaintenance
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Maintenance tables created successfully!")

if __name__ == "__main__":
    create_maintenance_tables()
