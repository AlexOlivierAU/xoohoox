#!/usr/bin/env python3
"""
Database initialization script for Xoohoox Juice Production Management System
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.models.batch_tracking import BatchTracking
from app.models.quality_control import QualityControl
from app.models.equipment_maintenance import EquipmentMaintenance
from app.models.equipment import Equipment
from app.models.inventory_management import InventoryManagement

def init_database():
    """Initialize the database with tables and sample data"""
    
    # Create engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we already have data
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Adding sample data...")
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@xoohoox.com",
            full_name="System Administrator",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8J5QKq",  # password: admin123
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        
        # Create sample equipment
        equipment1 = Equipment(
            name="Juice Press 1",
            equipment_type="juice_press",
            location="Production Line A",
            status="operational",
            manufacturer="JuiceTech",
            model="JP-2000",
            serial_number="JP001-2024",
            installation_date="2024-01-01"
        )
        equipment2 = Equipment(
            name="Fermentation Tank 1",
            equipment_type="fermentation_tank",
            location="Fermentation Room",
            status="operational",
            manufacturer="FermentCorp",
            model="FT-5000",
            serial_number="FT001-2024",
            installation_date="2024-01-01"
        )
        db.add(equipment1)
        db.add(equipment2)
        
        # Create sample batch
        batch1 = BatchTracking(
            batch_id="B001",
            fruit_type="Apple",
            quantity=1000.0,
            unit="L",
            status="active",
            quality_grade="A",
            created_by="admin",
            updated_by="admin"
        )
        db.add(batch1)
        
        # Create sample inventory items
        inventory1 = InventoryManagement(
            item_id="INV001",
            item_name="Apples",
            item_type="Raw Material",
            description="Fresh apples for juicing",
            unit_of_measure="kg",
            quantity_in_stock=500.0,
            minimum_stock_level=100.0,
            reorder_point=150.0,
            maximum_stock_level=1000.0,
            storage_location="Cold Storage A",
            storage_condition="Refrigerated",
            status="In Stock",
            supplier_name="Fresh Fruits Co.",
            unit_cost=2.50
        )
        inventory2 = InventoryManagement(
            item_id="INV002",
            item_name="Sugar",
            item_type="Raw Material",
            description="Granulated sugar for sweetening",
            unit_of_measure="kg",
            quantity_in_stock=200.0,
            minimum_stock_level=50.0,
            reorder_point=75.0,
            maximum_stock_level=500.0,
            storage_location="Dry Storage",
            storage_condition="Ambient",
            status="In Stock",
            supplier_name="Sweet Supplies",
            unit_cost=1.80
        )
        db.add(inventory1)
        db.add(inventory2)
        
        # Commit all changes
        db.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 