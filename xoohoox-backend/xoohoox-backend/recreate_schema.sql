-- XooHooX Database Schema Recreation Script
-- This script will drop and recreate the entire database schema

-- Drop all existing tables and types
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- Create enum types
CREATE TYPE fruittype AS ENUM ('APPLE', 'PEAR', 'GRAPE', 'MIXED', 'OTHER');
CREATE TYPE batchstatus AS ENUM ('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'FAILED');
CREATE TYPE qualitygrade AS ENUM ('A', 'B', 'C', 'REJECT');
CREATE TYPE juicetype AS ENUM ('APPLE', 'PEAR', 'GRAPE', 'MIXED');
CREATE TYPE processstatus AS ENUM ('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED');
CREATE TYPE transformationtype AS ENUM ('CHEMISTRY_PREP', 'HEAT_ACTIVATION', 'INITIAL_FERMENTATION', 'UPSCALE_FERMENTATION', 'VINEGAR_PROCESSING', 'DISTILLATION', 'STAGE_2_PROCESSING', 'DRYING', 'COMPOSTING', 'MARKET_SALE', 'OTHER');
CREATE TYPE juiceprocessingtype AS ENUM ('JP1', 'JP2', 'JP3', 'JP4', 'JP5');
CREATE TYPE pathtaken AS ENUM ('vinegar', 'distillation', 'archived');
CREATE TYPE juicevariant AS ENUM ('JP1', 'JP2', 'JP3', 'JP4', 'JP5');
CREATE TYPE upscalestage AS ENUM ('Test 4', 'Test 5', 'Test 6');
CREATE TYPE upscalestatus AS ENUM ('pending', 'complete', 'failed');
CREATE TYPE itemtype AS ENUM ('RAW_MATERIAL', 'PACKAGING', 'CHEMICAL', 'EQUIPMENT', 'CONSUMABLE');
CREATE TYPE storagecondition AS ENUM ('AMBIENT', 'REFRIGERATED', 'FROZEN', 'CONTROLLED');
CREATE TYPE inventorystatus AS ENUM ('ACTIVE', 'INACTIVE', 'DISCONTINUED');

-- 1. Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Farms table
CREATE TABLE farms (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    contact_info VARCHAR,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Yeast Strains table
CREATE TABLE yeast_strains (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    supplier VARCHAR,
    temperature_range VARCHAR,
    alcohol_tolerance FLOAT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Batch table
CREATE TABLE batch (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Batch Tracking table
CREATE TABLE batch_tracking (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    fruit_type fruittype NOT NULL,
    process_type VARCHAR NOT NULL,
    grower_id VARCHAR,
    status VARCHAR DEFAULT 'planned',
    stage VARCHAR DEFAULT 'initial',
    progress FLOAT DEFAULT 0.0,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    quality_checks JSON DEFAULT '[]',
    maintenance_records JSON DEFAULT '[]',
    environmental_impact JSON,
    processing_start_date TIMESTAMP,
    processing_end_date TIMESTAMP,
    final_product_quantity FLOAT,
    production_date TIMESTAMP,
    recipe_id INTEGER,
    ingredients JSON DEFAULT '[]',
    juice_type juicetype NOT NULL,
    target_quantity FLOAT NOT NULL,
    actual_quantity FLOAT,
    completion_date TIMESTAMP,
    quality_grade qualitygrade,
    actual_ingredients JSON,
    temperature FLOAT,
    ph_level FLOAT,
    brix FLOAT,
    processing_time INTEGER,
    issues JSON,
    corrective_actions JSON,
    created_by VARCHAR NOT NULL,
    updated_by VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Batch Dispatches table
CREATE TABLE batch_dispatches (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR UNIQUE NOT NULL,
    grower_id INTEGER NOT NULL,
    produce_type VARCHAR NOT NULL,
    varietal VARCHAR NOT NULL,
    dispatch_date DATE NOT NULL,
    quantity_kg FLOAT NOT NULL
);

-- 7. Fermentation Trials table
CREATE TABLE fermentation_trials (
    id SERIAL PRIMARY KEY,
    trial_id VARCHAR UNIQUE,
    batch_id INTEGER REFERENCES batch(id),
    yeast_strain VARCHAR,
    juice_variant juicevariant,
    initial_volume FLOAT,
    sg FLOAT,
    ph FLOAT,
    brix FLOAT,
    current_abv FLOAT,
    path_taken pathtaken,
    status VARCHAR,
    daily_readings JSON DEFAULT '[]',
    upscale_history JSON DEFAULT '[]',
    compound_results JSON DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Upscale Runs table
CREATE TABLE upscale_runs (
    id SERIAL PRIMARY KEY,
    upscale_id VARCHAR UNIQUE,
    trial_id INTEGER REFERENCES fermentation_trials(id),
    stage upscalestage,
    volume FLOAT,
    yield_amount FLOAT,
    abv_result FLOAT,
    compound_summary VARCHAR,
    status upscalestatus DEFAULT 'pending',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Transformation Stages table
CREATE TABLE transformation_stages (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR,
    stage_number INTEGER NOT NULL,
    stage_name VARCHAR NOT NULL,
    stage_type transformationtype NOT NULL,
    status batchstatus NOT NULL,
    total_trials INTEGER DEFAULT 1,
    trials_to_proceed INTEGER,
    parent_stage_id INTEGER REFERENCES transformation_stages(id),
    upscale_factor DECIMAL(5,2),
    target_volume DECIMAL(10,2),
    planned_duration_days INTEGER,
    actual_duration_days DECIMAL(5,1),
    branching_rule VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. Juicing Results table
CREATE TABLE juicing_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    juice_processing_type juiceprocessingtype NOT NULL,
    is_raw_juice_ferment BOOLEAN DEFAULT FALSE,
    input_weight DECIMAL(10,3),
    fruit_condition VARCHAR,
    juice_volume DECIMAL(10,2) NOT NULL,
    juice_yield DECIMAL(5,2),
    juice_yield_per_gram DECIMAL(8,4),
    brix DECIMAL(5,2) NOT NULL,
    ph DECIMAL(4,2) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    press_pressure DECIMAL(6,2),
    press_time DECIMAL(8,2),
    maceration_time DECIMAL(8,2),
    extraction_method VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Chemistry Results table
CREATE TABLE chemistry_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    ph_initial DECIMAL(4,2),
    ph_adjusted DECIMAL(4,2),
    titratable_acidity DECIMAL(5,2),
    sulfite_addition DECIMAL(8,2),
    nutrient_addition DECIMAL(8,2),
    enzyme_addition DECIMAL(8,2),
    clarification_agent VARCHAR,
    clarification_amount DECIMAL(8,2),
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. Heat Activation Results table
CREATE TABLE heat_activation_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    heating_method VARCHAR,
    target_temperature DECIMAL(5,2),
    actual_temperature DECIMAL(5,2),
    heating_duration INTEGER,
    cooling_method VARCHAR,
    final_temperature DECIMAL(5,2),
    post_heat_ph DECIMAL(4,2),
    clarity_improvement VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. Fermentation Results table
CREATE TABLE fermentation_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    initial_gravity DECIMAL(6,3),
    final_gravity DECIMAL(6,3),
    abv DECIMAL(4,2),
    temperature DECIMAL(5,2),
    ph DECIMAL(4,2),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 14. Vinegar Results table
CREATE TABLE vinegar_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    mother_culture_source VARCHAR,
    mother_culture_amount DECIMAL(8,2),
    initial_abv DECIMAL(4,2),
    target_acidity DECIMAL(4,2),
    actual_acidity DECIMAL(4,2),
    fermentation_days INTEGER,
    temperature_range VARCHAR,
    ph_progression JSON,
    taste_profile VARCHAR,
    clarity VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 15. Distillation Results table
CREATE TABLE distillation_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    distillation_type VARCHAR,
    wash_volume DECIMAL(8,2),
    heads_volume DECIMAL(8,2),
    hearts_volume DECIMAL(8,2),
    tails_volume DECIMAL(8,2),
    collection_abv DECIMAL(4,2),
    cuts_made VARCHAR,
    temperature_profile JSON,
    reflux_ratio DECIMAL(4,2),
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 16. Stage 2 Results table
CREATE TABLE stage2_results (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    aging_method VARCHAR,
    aging_duration_days INTEGER,
    container_type VARCHAR,
    container_size DECIMAL(8,2),
    final_abv DECIMAL(4,2),
    color_development VARCHAR,
    flavor_notes VARCHAR,
    filtration_applied BOOLEAN,
    bottling_date DATE,
    bottle_count INTEGER,
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 17. Fruit Performance table
CREATE TABLE fruit_performance (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER REFERENCES transformation_stages(id),
    fruit_variety VARCHAR,
    harvest_date DATE,
    storage_duration_days INTEGER,
    ripeness_score INTEGER,
    damage_assessment VARCHAR,
    juice_yield_actual DECIMAL(5,2),
    juice_yield_expected DECIMAL(5,2),
    sugar_content_brix DECIMAL(5,2),
    acid_content DECIMAL(5,2),
    overall_quality_score INTEGER,
    notes VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 18. Juicing Input Log table
CREATE TABLE juicing_input_log (
    id SERIAL PRIMARY KEY,
    log_id VARCHAR UNIQUE NOT NULL,
    batch_id VARCHAR REFERENCES batch_tracking(batch_id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    operator_id INTEGER,
    equipment_id VARCHAR,
    input_quantity_kg FLOAT NOT NULL,
    output_quantity_kg FLOAT,
    process_status processstatus,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 19. Quality Control table
CREATE TABLE quality_control (
    id SERIAL PRIMARY KEY,
    test_id VARCHAR UNIQUE NOT NULL,
    batch_id VARCHAR REFERENCES batch_tracking(batch_id),
    test_type VARCHAR NOT NULL,
    test_date TIMESTAMP NOT NULL,
    test_name VARCHAR NOT NULL,
    test_method VARCHAR,
    test_parameters JSON,
    expected_range_min FLOAT,
    expected_range_max FLOAT,
    actual_value FLOAT,
    unit_of_measure VARCHAR,
    result VARCHAR,
    tester_id INTEGER,
    equipment_used VARCHAR,
    temperature_c FLOAT,
    humidity_percent FLOAT,
    notes TEXT,
    corrective_actions TEXT,
    retest_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 20. Equipment table
CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    equipment_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    type VARCHAR,
    manufacturer VARCHAR,
    model VARCHAR,
    serial_number VARCHAR,
    purchase_date DATE,
    warranty_expiry DATE,
    status VARCHAR DEFAULT 'active',
    location VARCHAR,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 21. Equipment Maintenance table
CREATE TABLE equipment_maintenance (
    id SERIAL PRIMARY KEY,
    maintenance_id VARCHAR UNIQUE NOT NULL,
    equipment_id VARCHAR,
    equipment_type VARCHAR,
    equipment_name VARCHAR,
    manufacturer VARCHAR,
    model_number VARCHAR,
    serial_number VARCHAR,
    installation_date TIMESTAMP,
    maintenance_type VARCHAR,
    maintenance_status VARCHAR,
    scheduled_date TIMESTAMP,
    actual_date TIMESTAMP,
    technician_id INTEGER,
    cost FLOAT,
    parts_replaced TEXT,
    work_performed TEXT,
    results TEXT,
    next_maintenance_date TIMESTAMP,
    requires_shutdown BOOLEAN DEFAULT FALSE,
    shutdown_duration_hours FLOAT,
    notes TEXT,
    is_critical BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 22. Maintenance Log table
CREATE TABLE maintenance_log (
    id SERIAL PRIMARY KEY,
    equipment_id VARCHAR NOT NULL,
    maintenance_date TIMESTAMP NOT NULL,
    maintenance_type VARCHAR NOT NULL,
    performed_by VARCHAR NOT NULL,
    description TEXT,
    cost DECIMAL(10,2),
    next_maintenance_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 23. Inventory Management table
CREATE TABLE inventory_management (
    id SERIAL PRIMARY KEY,
    item_id VARCHAR UNIQUE NOT NULL,
    item_name VARCHAR NOT NULL,
    item_type itemtype,
    description TEXT,
    sku VARCHAR UNIQUE,
    barcode VARCHAR UNIQUE,
    unit_of_measure VARCHAR,
    quantity_in_stock FLOAT DEFAULT 0,
    minimum_stock_level FLOAT DEFAULT 0,
    reorder_point FLOAT DEFAULT 0,
    maximum_stock_level FLOAT,
    storage_location VARCHAR,
    storage_condition storagecondition,
    status inventorystatus DEFAULT 'ACTIVE',
    supplier_id VARCHAR,
    supplier_name VARCHAR,
    unit_cost FLOAT,
    last_ordered_date TIMESTAMP,
    last_received_date TIMESTAMP,
    expiry_date TIMESTAMP,
    lot_number VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    total_received FLOAT DEFAULT 0,
    total_issued FLOAT DEFAULT 0,
    total_adjusted FLOAT DEFAULT 0,
    last_count_date TIMESTAMP,
    last_count_quantity FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 24. Evaluations table
CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR,
    evaluator_name VARCHAR NOT NULL,
    evaluation_date TIMESTAMP NOT NULL,
    evaluation_type VARCHAR,
    scores JSON,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 25. Fermentation Logs table
CREATE TABLE fermentation_logs (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR,
    log_date TIMESTAMP NOT NULL,
    temperature FLOAT,
    specific_gravity FLOAT,
    ph FLOAT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 26. Juicing Logs table
CREATE TABLE juicing_logs (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR,
    juicing_date TIMESTAMP NOT NULL,
    method VARCHAR,
    yield_percentage FLOAT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_batch_tracking_batch_id ON batch_tracking(batch_id);
CREATE INDEX idx_batch_tracking_status ON batch_tracking(status);
CREATE INDEX idx_fermentation_trials_batch_id ON fermentation_trials(batch_id);
CREATE INDEX idx_quality_control_batch_id ON quality_control(batch_id);
CREATE INDEX idx_juicing_input_log_batch_id ON juicing_input_log(batch_id);
CREATE INDEX idx_transformation_stages_batch_id ON transformation_stages(batch_id);
CREATE INDEX idx_equipment_maintenance_equipment_id ON equipment_maintenance(equipment_id);
CREATE INDEX idx_inventory_management_item_id ON inventory_management(item_id);

-- Create alembic version table for migration tracking
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Summary
SELECT 'Schema recreation completed successfully!' as status;
