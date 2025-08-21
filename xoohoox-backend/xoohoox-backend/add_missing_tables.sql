-- Add missing tables to reach 500+ fields

-- 27. Failure Reports table
CREATE TABLE failure_reports (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    date_reported TIMESTAMP NOT NULL,
    process_stage VARCHAR NOT NULL,
    failure_type VARCHAR NOT NULL,
    cause TEXT,
    action_taken TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    evaluator_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 28. Fermentation Kinetics table
CREATE TABLE fermentation_kinetics (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    start_date TIMESTAMP NOT NULL,
    initial_brix FLOAT,
    initial_ph FLOAT,
    initial_temp FLOAT,
    yeast_strain VARCHAR,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 29. Fermentation Plan table
CREATE TABLE fermentation_plan (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    grower VARCHAR,
    produce VARCHAR,
    varietal VARCHAR,
    start_date TIMESTAMP,
    brix_target FLOAT,
    ph_target FLOAT,
    temp_target_c FLOAT,
    yeast_strain VARCHAR,
    substrate_notes TEXT,
    hypothesis_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 30. Liquefaction Method table
CREATE TABLE liquefaction_method (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    liquefier_product VARCHAR,
    method_steps TEXT,
    timing_notes TEXT,
    produce_constraints TEXT,
    required_conditions TEXT,
    testing_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 31. Liquefaction Plan table
CREATE TABLE liquefaction_plan (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    grower VARCHAR,
    produce VARCHAR,
    varietal VARCHAR,
    target_yield_ml FLOAT,
    substrate_type VARCHAR,
    liquefier_type VARCHAR,
    hypothesis_notes TEXT,
    start_date TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 32. Liquefaction Runs table
CREATE TABLE liquefaction_runs (
    id SERIAL PRIMARY KEY,
    grower VARCHAR,
    produce VARCHAR,
    varietal VARCHAR,
    batch_id VARCHAR NOT NULL,
    test_stage VARCHAR,
    extraction_point VARCHAR,
    extraction_start_date TIMESTAMP,
    extraction_yield_ml FLOAT,
    extraction_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 33. Produce Preliminary Evaluation table
CREATE TABLE produce_prelim_eval (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    grower VARCHAR,
    produce VARCHAR,
    varietal VARCHAR,
    harvest_date DATE,
    collection_method VARCHAR,
    ripeness VARCHAR,
    visible_damage TEXT,
    contamination_notes TEXT,
    color_notes TEXT,
    odor_notes TEXT,
    firmness_notes TEXT,
    overall_score INTEGER,
    evaluator_name VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 34. Product Evaluation table
CREATE TABLE product_evaluation (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    clarity_score INTEGER,
    acidity_ph FLOAT,
    aroma_notes TEXT,
    flavour_notes TEXT,
    viscosity_notes TEXT,
    classification_result VARCHAR,
    evaluator_name VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 35. Sensory Feedback table
CREATE TABLE sensory_feedback (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    panelist_type VARCHAR,
    date TIMESTAMP,
    clarity_score INTEGER,
    aroma_notes TEXT,
    taste_notes TEXT,
    mouthfeel_notes TEXT,
    rating INTEGER,
    suggested_use VARCHAR,
    evaluator_name VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 36. Vinegar Kinetics table
CREATE TABLE vinegar_kinetics (
    id SERIAL PRIMARY KEY,
    grower VARCHAR,
    produce VARCHAR,
    varietal VARCHAR,
    batch_id VARCHAR NOT NULL,
    test_stage VARCHAR,
    substrate_type VARCHAR,
    start_date TIMESTAMP,
    acetic_acid_target FLOAT,
    ph_initial FLOAT,
    ph_final FLOAT,
    vinegar_yield_ml FLOAT,
    vinegar_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 37. Additional Distillation Results table (from documentation)
CREATE TABLE distillation_results_detailed (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    date TIMESTAMP,
    distiller_name VARCHAR,
    fruit_type VARCHAR,
    varietal VARCHAR,
    wash_volume_l FLOAT,
    distillate_volume_ml FLOAT,
    heads_volume_ml FLOAT,
    hearts_volume_ml FLOAT,
    tails_volume_ml FLOAT,
    peak_temp_c FLOAT,
    abv_collected_percent FLOAT,
    clarity_notes TEXT,
    aroma_notes TEXT,
    final_use_class VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 38. Additional Fermentation Results table (from documentation)
CREATE TABLE fermentation_results_detailed (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    evaluator_name VARCHAR,
    evaluation_date TIMESTAMP,
    final_abv FLOAT,
    final_ph FLOAT,
    clarity_score INTEGER,
    color_notes TEXT,
    smell_notes TEXT,
    taste_notes TEXT,
    fermentation_result VARCHAR,
    additional_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 39. Additional Juicing Results table (from documentation)
CREATE TABLE juicing_results_detailed (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    amount_frozen_kg FLOAT,
    defrost_start_time TIMESTAMP,
    defrost_finish_time TIMESTAMP,
    defrost_duration INTEGER,
    clarified_volume_ml FLOAT,
    clarified_yield_ratio FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 40. Additional Juicing Input Log table (from documentation)
CREATE TABLE juicing_input_log_detailed (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    grower VARCHAR,
    produce VARCHAR,
    varietal VARCHAR,
    weight_before_juicing FLOAT,
    juice_volume FLOAT,
    juice_clarity VARCHAR,
    separation_observed BOOLEAN,
    method_used VARCHAR,
    date_collected TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for new tables
CREATE INDEX idx_failure_reports_batch_id ON failure_reports(batch_id);
CREATE INDEX idx_fermentation_kinetics_batch_id ON fermentation_kinetics(batch_id);
CREATE INDEX idx_fermentation_plan_batch_id ON fermentation_plan(batch_id);
CREATE INDEX idx_liquefaction_method_batch_id ON liquefaction_method(batch_id);
CREATE INDEX idx_liquefaction_plan_batch_id ON liquefaction_plan(batch_id);
CREATE INDEX idx_liquefaction_runs_batch_id ON liquefaction_runs(batch_id);
CREATE INDEX idx_produce_prelim_eval_batch_id ON produce_prelim_eval(batch_id);
CREATE INDEX idx_product_evaluation_batch_id ON product_evaluation(batch_id);
CREATE INDEX idx_sensory_feedback_batch_id ON sensory_feedback(batch_id);
CREATE INDEX idx_vinegar_kinetics_batch_id ON vinegar_kinetics(batch_id);

-- Summary
SELECT 'Additional tables added successfully!' as status;
