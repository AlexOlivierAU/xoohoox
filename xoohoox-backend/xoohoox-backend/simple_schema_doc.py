#!/usr/bin/env python3
"""
Simple database schema documentation generator
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def generate_simple_schema_doc():
    """Generate simple database schema documentation"""
    
    print("# XooHooX Database Schema Overview")
    print("Generated from SQLAlchemy models\n")
    
    # Define the tables and their columns based on the model files
    schema = {
        "users": {
            "description": "User management and authentication",
            "columns": [
                "id (Integer, PK)",
                "email (String, unique)",
                "username (String, unique)", 
                "hashed_password (String)",
                "full_name (String)",
                "is_active (Boolean)",
                "is_superuser (Boolean)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "batch_tracking": {
            "description": "Main batch tracking and processing",
            "columns": [
                "id (Integer, PK)",
                "batch_id (String, unique)",
                "name (String)",
                "fruit_type (Enum)",
                "process_type (String)",
                "grower_id (String)",
                "status (String)",
                "stage (String)",
                "progress (Float)",
                "start_date (DateTime)",
                "end_date (DateTime)",
                "quality_checks (JSON)",
                "maintenance_records (JSON)",
                "environmental_impact (JSON)",
                "processing_start_date (DateTime)",
                "processing_end_date (DateTime)",
                "final_product_quantity (Float)",
                "production_date (DateTime)",
                "recipe_id (Integer)",
                "ingredients (JSON)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "fermentation_trials": {
            "description": "Fermentation trial experiments",
            "columns": [
                "id (Integer, PK)",
                "trial_id (String, unique)",
                "batch_id (String)",
                "yeast_strain (String)",
                "initial_brix (Float)",
                "initial_ph (Float)",
                "initial_temp (Float)",
                "start_date (DateTime)",
                "end_date (DateTime)",
                "status (Enum)",
                "notes (Text)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "upscale_runs": {
            "description": "Upscale production runs",
            "columns": [
                "id (Integer, PK)",
                "upscale_id (String, unique)",
                "trial_id (Integer, FK)",
                "stage (Enum)",
                "volume (Float)",
                "yield_amount (Float)",
                "abv_result (Float)",
                "compound_summary (String)",
                "status (Enum)",
                "timestamp (DateTime)"
            ]
        },
        "quality_control": {
            "description": "Quality control tests and results",
            "columns": [
                "id (Integer, PK)",
                "test_id (String, unique)",
                "batch_id (String)",
                "test_type (String)",
                "test_date (DateTime)",
                "test_name (String)",
                "test_method (String)",
                "test_parameters (JSON)",
                "expected_range_min (Float)",
                "expected_range_max (Float)",
                "actual_value (Float)",
                "unit_of_measure (String)",
                "result (String)",
                "tester_id (Integer)",
                "equipment_used (String)",
                "temperature_c (Float)",
                "humidity_percent (Float)",
                "notes (Text)",
                "corrective_actions (Text)",
                "retest_required (Boolean)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "equipment_maintenance": {
            "description": "Equipment maintenance records",
            "columns": [
                "id (Integer, PK)",
                "maintenance_id (String, unique)",
                "equipment_id (String)",
                "equipment_type (String)",
                "equipment_name (String)",
                "manufacturer (String)",
                "model_number (String)",
                "serial_number (String)",
                "installation_date (DateTime)",
                "maintenance_type (String)",
                "maintenance_status (String)",
                "scheduled_date (DateTime)",
                "actual_date (DateTime)",
                "technician_id (Integer)",
                "cost (Float)",
                "parts_replaced (Text)",
                "work_performed (Text)",
                "results (Text)",
                "next_maintenance_date (DateTime)",
                "requires_shutdown (Boolean)",
                "shutdown_duration_hours (Float)",
                "notes (Text)",
                "is_critical (Boolean)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "inventory_management": {
            "description": "Inventory tracking and management",
            "columns": [
                "id (Integer, PK)",
                "item_id (String, unique)",
                "item_name (String)",
                "item_type (Enum)",
                "description (Text)",
                "sku (String, unique)",
                "barcode (String, unique)",
                "unit_of_measure (String)",
                "quantity_in_stock (Float)",
                "minimum_stock_level (Float)",
                "reorder_point (Float)",
                "maximum_stock_level (Float)",
                "storage_location (String)",
                "storage_condition (Enum)",
                "status (Enum)",
                "supplier_id (String)",
                "supplier_name (String)",
                "unit_cost (Float)",
                "last_ordered_date (DateTime)",
                "last_received_date (DateTime)",
                "expiry_date (DateTime)",
                "lot_number (String)",
                "is_active (Boolean)",
                "notes (Text)",
                "total_received (Float)",
                "total_issued (Float)",
                "total_adjusted (Float)",
                "last_count_date (DateTime)",
                "last_count_quantity (Float)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "juicing_input_log": {
            "description": "Juicing process input logs",
            "columns": [
                "id (Integer, PK)",
                "log_id (String, unique)",
                "batch_id (String)",
                "timestamp (DateTime)",
                "operator_id (Integer)",
                "equipment_id (String)",
                "input_quantity_kg (Float)",
                "output_quantity_kg (Float)",
                "process_status (String)",
                "notes (Text)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "transformation_stages": {
            "description": "Production transformation stages",
            "columns": [
                "id (Integer, PK)",
                "batch_id (String)",
                "stage_number (Integer)",
                "stage_name (String)",
                "start_date (DateTime)",
                "end_date (DateTime)",
                "notes (Text)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "juicing_results": {
            "description": "Juicing process results",
            "columns": [
                "id (Integer, PK)",
                "stage_id (Integer, FK)",
                "juice_volume (Float)",
                "juice_yield (Float)",
                "brix (Float)",
                "ph (Float)",
                "notes (Text)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        },
        "fermentation_results": {
            "description": "Fermentation process results",
            "columns": [
                "id (Integer, PK)",
                "stage_id (Integer, FK)",
                "initial_gravity (Float)",
                "final_gravity (Float)",
                "abv (Float)",
                "temperature (Float)",
                "ph (Float)",
                "notes (Text)",
                "created_at (DateTime)",
                "updated_at (DateTime)"
            ]
        }
    }
    
    print("## Database Tables\n")
    
    for table_name, table_info in schema.items():
        print(f"### {table_name}")
        print(f"**Description**: {table_info['description']}")
        print()
        print("**Columns:**")
        for column in table_info['columns']:
            print(f"- {column}")
        print()
        print("---\n")
    
    print("## Key Relationships")
    print()
    print("- **batch_tracking** → **juicing_input_log** (one-to-many)")
    print("- **batch_tracking** → **quality_control** (one-to-many)")
    print("- **fermentation_trials** → **upscale_runs** (one-to-many)")
    print("- **transformation_stages** → **juicing_results** (one-to-many)")
    print("- **transformation_stages** → **fermentation_results** (one-to-many)")
    print()
    
    print("## Summary")
    print(f"Total tables: {len(schema)}")
    print()
    print("**Core Tables:**")
    print("- `batch_tracking` - Main batch management")
    print("- `fermentation_trials` - Experimental trials")
    print("- `upscale_runs` - Production scaling")
    print("- `quality_control` - Quality testing")
    print("- `equipment_maintenance` - Equipment management")
    print("- `inventory_management` - Stock tracking")

if __name__ == "__main__":
    generate_simple_schema_doc()
