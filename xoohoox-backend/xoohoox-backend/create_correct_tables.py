#!/usr/bin/env python3
"""
Create maintenance-related tables with correct structure
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models.equipment import Equipment
from app.models.maintenance_log import MaintenanceLog
from app.models.equipment_maintenance import EquipmentMaintenance
from app.models.base import Base

def create_correct_tables():
    """Create tables with the correct structure"""
    print("Creating tables with correct structure...")
    
    # Create database engine as postgres user
    postgres_uri = "postgresql://postgres@localhost:5432/xoohoox"
    engine = create_engine(
        postgres_uri,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={"options": "-c search_path=public"}
    )
    
    # Import the models to register them with SQLAlchemy
    _ = Equipment
    _ = MaintenanceLog
    _ = EquipmentMaintenance
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Grant permissions
    with engine.connect() as conn:
        conn.execute(text('GRANT USAGE ON SCHEMA public TO xoohoox'))
        conn.execute(text('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO xoohoox'))
        conn.execute(text('GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO xoohoox'))
        conn.commit()
    
    print("Tables created successfully with correct structure!")

if __name__ == "__main__":
    create_correct_tables()
