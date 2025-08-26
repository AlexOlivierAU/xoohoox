#!/usr/bin/env python3
"""
Script to create all database tables from models
"""

import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def create_all_tables():
    """Create all tables from models"""
    
    print("Importing models...")
    
    # Import all models to register them with SQLAlchemy
    from app.models.user import User
    from app.models.batch_tracking import BatchTracking
    from app.models.batch_dispatch import BatchDispatch
    from app.models.batch import Batch
    from app.models.yeast_strain import YeastStrain
    from app.models.evaluation import Evaluation
    from app.models.fermentation_log import FermentationLog
    from app.models.juicing_log import JuicingLog
    from app.models.farm import Farm
    from app.models.upscale import UpscaleRun
    from app.models.equipment import Equipment
    from app.models.maintenance_log import MaintenanceLog
    from app.models.equipment_maintenance import EquipmentMaintenance
    from app.models.transformation import (
        TransformationStage, JuicingResults, ChemistryResults, 
        HeatActivationResults, FermentationResults, VinegarResults,
        DistillationResults, Stage2Results, FruitPerformance
    )
    from app.models.juicing_input_log import JuicingInputLog
    from app.models.inventory_management import InventoryManagement
    from app.models.quality_control import QualityControl
    from app.models.fermentation_trial import FermentationTrial
    
    print("Models imported successfully")
    
    # Import database engine and base
    from app.db.base_class import Base
    from app.core.config import settings
    from sqlalchemy import create_engine
    
    print(f"Database URL: {settings.SQLALCHEMY_DATABASE_URI}")
    
    # Create engine with schema
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Set schema explicitly
    with engine.connect() as conn:
        from sqlalchemy import text
        conn.execute(text("SET search_path TO public;"))
        conn.commit()
    
    print(f"Number of tables in metadata: {len(Base.metadata.tables)}")
    print("Tables to be created:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")
    
    # Drop all tables first
    print("\nDropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("All tables created successfully!")

if __name__ == "__main__":
    create_all_tables()
