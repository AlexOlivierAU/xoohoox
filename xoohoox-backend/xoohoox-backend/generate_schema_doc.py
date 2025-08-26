#!/usr/bin/env python3
"""
Generate database schema documentation from SQLAlchemy models
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def generate_schema_doc():
    """Generate comprehensive database schema documentation"""
    
    print("# XooHooX Database Schema Documentation")
    print("Generated from SQLAlchemy models\n")
    
    # Import all models
    try:
        from app.models.base import BaseModel
        from app.models.user import User
        from app.models.batch_tracking import BatchTracking
        from app.models.quality_control import QualityControl
        from app.models.equipment_maintenance import EquipmentMaintenance
        from app.models.inventory_management import InventoryManagement
        from app.models.juicing_input_log import JuicingInputLog
        from app.models.fermentation_trial import FermentationTrial
        from app.models.upscale import UpscaleRun
        from app.models.equipment import Equipment
        from app.models.maintenance_log import MaintenanceLog
        from app.models.batch_dispatch import BatchDispatch
        from app.models.farm import Farm
        from app.models.yeast_strain import YeastStrain
        from app.models.evaluation import Evaluation
        from app.models.fermentation_log import FermentationLog
        from app.models.juicing_log import JuicingLog
        from app.models.transformation import TransformationStage, JuicingResult, FermentationResult
        
        models = [
            User, BatchTracking, QualityControl, EquipmentMaintenance,
            InventoryManagement, JuicingInputLog, FermentationTrial,
            UpscaleRun, Equipment, MaintenanceLog, BatchDispatch, Farm,
            YeastStrain, Evaluation, FermentationLog, JuicingLog,
            TransformationStage, JuicingResult, FermentationResult
        ]
        
        print("## Database Tables\n")
        
        for model in models:
            if hasattr(model, '__tablename__'):
                table_name = model.__tablename__
            else:
                table_name = model.__name__.lower()
            
            print(f"### {table_name}")
            print(f"**Model**: `{model.__name__}`")
            print()
            
            # Get columns
            columns = []
            for column in model.__table__.columns:
                col_info = {
                    'name': column.name,
                    'type': str(column.type),
                    'nullable': column.nullable,
                    'primary_key': column.primary_key,
                    'unique': column.unique,
                    'default': column.default,
                    'index': column.index
                }
                columns.append(col_info)
            
            print("| Column | Type | Nullable | Primary Key | Unique | Index | Default |")
            print("|--------|------|----------|-------------|--------|-------|---------|")
            
            for col in columns:
                nullable = "✓" if col['nullable'] else "✗"
                primary = "✓" if col['primary_key'] else "✗"
                unique = "✓" if col['unique'] else "✗"
                index = "✓" if col['index'] else "✗"
                default = str(col['default']) if col['default'] is not None else ""
                
                print(f"| {col['name']} | {col['type']} | {nullable} | {primary} | {unique} | {index} | {default} |")
            
            print()
            
            # Show relationships if any
            relationships = []
            for attr_name in dir(model):
                attr = getattr(model, attr_name)
                if hasattr(attr, 'property') and hasattr(attr.property, 'mapper'):
                    relationships.append(attr_name)
            
            if relationships:
                print("**Relationships:**")
                for rel in relationships:
                    print(f"- `{rel}`")
                print()
            
            print("---\n")
        
        print("## Summary")
        print(f"Total tables: {len(models)}")
        
    except ImportError as e:
        print(f"Error importing models: {e}")
        print("Make sure you're in the correct directory and all dependencies are installed.")
    except Exception as e:
        print(f"Error generating schema: {e}")

if __name__ == "__main__":
    generate_schema_doc()
