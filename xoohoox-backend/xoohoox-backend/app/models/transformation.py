from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum as SQLEnum, Boolean, Numeric
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import YeastStrain, BatchStatus

class TransformationType(str, Enum):
    CHEMISTRY_PREP = "CHEMISTRY_PREP"  # Phase 1: Raw Material & Chemistry Prep
    HEAT_ACTIVATION = "HEAT_ACTIVATION"  # Phase 2: Heat Activation & Nutrient Prep
    INITIAL_FERMENTATION = "INITIAL_FERMENTATION"  # Phase 3: Initial Fermentation
    UPSCALE_FERMENTATION = "UPSCALE_FERMENTATION"  # Phase 4: Upscale Fermentation
    VINEGAR_PROCESSING = "VINEGAR_PROCESSING"  # Vinegar branch
    DISTILLATION = "DISTILLATION"  # Phase 4: Distillation Ladder
    STAGE_2_PROCESSING = "STAGE_2_PROCESSING"  # Stage 2 (Post Test 6)
    DRYING = "DRYING"
    COMPOSTING = "COMPOSTING"
    MARKET_SALE = "MARKET_SALE"
    OTHER = "OTHER"

class ProcessStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class JuiceProcessingType(str, Enum):
    JP1 = "JP1"  # Raw Juice (one-time only)
    JP2 = "JP2"  # Whole Fruit Macerate Juice
    JP3 = "JP3"  # Pressed Juice
    JP4 = "JP4"  # Extractor Juice
    JP5 = "JP5"  # Optional variations

class TransformationStage(Base):
    __tablename__ = "transformation_stages"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch_tracking.batch_id"))
    stage_number = Column(Integer, nullable=False)
    stage_name = Column(String, nullable=False)
    stage_type = Column(Enum(TransformationType), nullable=False)
    status = Column(Enum(BatchStatus), nullable=False)
    total_trials = Column(Integer, nullable=False, default=1)  # Total number of trials for this stage
    trials_to_proceed = Column(Integer, nullable=True)  # Number of trials that should proceed to next stage
    parent_stage_id = Column(Integer, ForeignKey("transformation_stages.id"), nullable=True)  # For linking upscale stages
    upscale_factor = Column(Numeric(5, 2), nullable=True)  # How much to upscale from previous stage (e.g., 10x)
    target_volume = Column(Numeric(10, 2), nullable=True)  # Target volume for this stage in milliliters
    planned_duration_days = Column(Integer, nullable=True)  # Planned duration in days
    actual_duration_days = Column(Numeric(5, 1), nullable=True)  # Actual duration in days (with decimal for partial days)
    branching_rule = Column(String, nullable=True)  # For vinegar path (8-13% ABV) or other branching logic
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    batch = relationship("BatchTracking", back_populates="transformation_stages")
    juicing_results = relationship("JuicingResults", back_populates="stage", uselist=False)
    chemistry_results = relationship("ChemistryResults", back_populates="stage", uselist=False)
    heat_activation_results = relationship("HeatActivationResults", back_populates="stage", uselist=False)
    fermentation_results = relationship("FermentationResults", back_populates="stage", uselist=False)
    vinegar_results = relationship("VinegarResults", back_populates="stage", uselist=False)
    distillation_results = relationship("DistillationResults", back_populates="stage", uselist=False)
    stage2_results = relationship("Stage2Results", back_populates="stage", uselist=False)
    fruit_performance = relationship("FruitPerformance", back_populates="stage", uselist=False)
    parent_stage = relationship("TransformationStage", remote_side=[id], backref="upscale_stages")

class JuicingResults(Base):
    __tablename__ = "juicing_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    
    # Juice processing variant
    juice_processing_type = Column(Enum(JuiceProcessingType), nullable=False)
    is_raw_juice_ferment = Column(Boolean, default=False)  # For JP1 (one-time only rule)
    
    # Input measurements
    input_weight = Column(Numeric(10, 3))  # in kg, 3 decimal places
    fruit_condition = Column(String)  # Description of fruit condition on arrival
    
    # Output measurements
    juice_volume = Column(Numeric(10, 2), nullable=False)  # in milliliters, 2 decimal places
    juice_yield = Column(Numeric(5, 2))  # percentage, 2 decimal places
    juice_yield_per_gram = Column(Numeric(8, 4))  # milliliters per gram, 4 decimal places
    brix = Column(Numeric(5, 2), nullable=False)  # sugar content, 2 decimal places
    ph = Column(Numeric(4, 2), nullable=False)  # pH, 2 decimal places
    temperature = Column(Numeric(5, 2), nullable=False)  # in Celsius, 2 decimal places
    
    # Process parameters
    press_pressure = Column(Numeric(6, 2), nullable=True)  # in bar, 2 decimal places
    press_time = Column(Numeric(8, 2), nullable=True)  # in minutes, 2 decimal places
    maceration_time = Column(Numeric(8, 2), nullable=True)  # in hours, 2 decimal places
    extraction_method = Column(String, nullable=True)  # Description of extraction method
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="juicing_results")

class ChemistryResults(Base):
    __tablename__ = "chemistry_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    
    # Initial readings
    initial_ph = Column(Numeric(4, 2), nullable=False)  # pH, 2 decimal places
    initial_sg = Column(Numeric(5, 4), nullable=False)  # specific gravity, 4 decimal places
    
    # Adjustments
    sodium_bicarb_added = Column(Numeric(6, 2), nullable=True)  # in kg, 2 decimal places
    reaction_time_hours = Column(Numeric(5, 2), nullable=True)  # in hours, 2 decimal places
    
    # Target values
    target_ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    target_sg = Column(Numeric(5, 4), nullable=True)  # specific gravity, 4 decimal places
    
    # Final readings
    final_ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    final_sg = Column(Numeric(5, 4), nullable=True)  # specific gravity, 4 decimal places
    
    # Process parameters
    batch_size = Column(Numeric(10, 2), nullable=True)  # in liters, 2 decimal places
    scale_up_notes = Column(Text, nullable=True)  # Notes about scaling up process
    no_adjustments_allowed = Column(Boolean, default=False)  # For raw juice ferments (JP1)
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="chemistry_results")

class HeatActivationResults(Base):
    __tablename__ = "heat_activation_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    
    # Heat activation parameters
    target_temperature = Column(Numeric(5, 2), nullable=False)  # in Celsius, 2 decimal places
    actual_temperature = Column(Numeric(5, 2), nullable=True)  # in Celsius, 2 decimal places
    rest_time_hours = Column(Numeric(5, 2), nullable=True)  # in hours, 2 decimal places
    
    # Nutrient and yeast preparation
    nutrient_concentration = Column(Numeric(5, 2), nullable=True)  # in g/L, 2 decimal places
    yeast_concentration = Column(Numeric(5, 2), nullable=True)  # in g/L, 2 decimal places
    rest_time_minutes = Column(Integer, nullable=True)  # in minutes
    
    # Pitch conditions
    pitch_temperature = Column(Numeric(5, 2), nullable=True)  # in Celsius, 2 decimal places
    pitch_ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    pitch_sg = Column(Numeric(5, 4), nullable=True)  # specific gravity, 4 decimal places
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="heat_activation_results")

class FermentationResults(Base):
    __tablename__ = "fermentation_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    trial_number = Column(Integer, nullable=False)  # Which trial number this is (1 to total_trials)
    proceeds_to_next_stage = Column(Boolean, default=False)  # Whether this trial should proceed
    parent_trial_id = Column(Integer, ForeignKey("fermentation_results.id"), nullable=True)  # For linking upscale trials
    upscale_batch = Column(String, nullable=True)  # Identifier for the upscale batch (e.g., "U1", "U2")
    
    # Yeast information
    yeast_strain = Column(String, nullable=False)  # Changed from Enum to String to allow any yeast type
    inoculation_date = Column(DateTime, nullable=False)
    yeast_source = Column(String, nullable=True)  # Where the yeast came from (e.g., "Previous upscale", "New culture")
    
    # Timing information
    planned_duration_days = Column(Integer, nullable=True)  # Planned duration in days
    actual_duration_days = Column(Numeric(5, 1), nullable=True)  # Actual duration in days
    completion_date = Column(DateTime, nullable=True)  # When the fermentation was completed
    lag_time_hours = Column(Numeric(5, 1), nullable=True)  # Time until fermentation starts (in hours)
    active_fermentation_days = Column(Numeric(5, 1), nullable=True)  # Duration of active fermentation
    
    # Fermentation timing factors
    temperature_control_method = Column(String, nullable=True)  # How temperature is controlled (e.g., "Room temp", "Water bath", "Incubator")
    temperature_variance = Column(Numeric(5, 2), nullable=True)  # How much temperature varied during fermentation
    nutrient_additions = Column(Text, nullable=True)  # Record of nutrient additions and timing
    aeration_frequency = Column(String, nullable=True)  # How often the must was aerated
    stuck_fermentation = Column(Boolean, default=False)  # Whether fermentation got stuck
    stuck_fermentation_resolution = Column(Text, nullable=True)  # How stuck fermentation was resolved
    restart_attempts = Column(Integer, nullable=True)  # Number of times fermentation was restarted
    
    # Initial measurements
    initial_volume = Column(Numeric(10, 2))  # in milliliters, 2 decimal places
    initial_gravity = Column(Numeric(5, 4), nullable=False)  # specific gravity, 4 decimal places
    initial_ph = Column(Numeric(4, 2))  # pH, 2 decimal places
    initial_temperature = Column(Numeric(5, 2))  # in Celsius, 2 decimal places
    
    # Ongoing measurements
    current_gravity = Column(Numeric(5, 4), nullable=True)  # specific gravity, 4 decimal places
    current_ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    current_temperature = Column(Numeric(5, 2), nullable=True)  # in Celsius, 2 decimal places
    
    # Final measurements
    final_gravity = Column(Numeric(5, 4), nullable=True)  # specific gravity, 4 decimal places
    final_ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    alcohol_content = Column(Numeric(5, 2), nullable=True)  # in percentage, 2 decimal places
    
    # Sensory evaluation
    aroma_notes = Column(Text, nullable=True)
    flavor_notes = Column(Text, nullable=True)
    clarity_rating = Column(Numeric(3, 1), nullable=True)  # 1-10 scale, 1 decimal place
    
    # Trial selection criteria
    selection_score = Column(Numeric(5, 2), nullable=True)  # Overall score for trial selection
    selection_notes = Column(Text, nullable=True)  # Notes about why this trial was selected
    
    # Upscale specific fields
    upscale_volume = Column(Numeric(10, 2), nullable=True)  # Volume used for next upscale in milliliters
    upscale_ratio = Column(Numeric(5, 2), nullable=True)  # Ratio of culture to new medium
    upscale_notes = Column(Text, nullable=True)  # Notes specific to upscaling process
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="fermentation_results")
    parent_trial = relationship("FermentationResults", remote_side=[id], backref="upscale_trials")

class VinegarResults(Base):
    __tablename__ = "vinegar_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    
    # Vinegar processing parameters
    vinegar_mother_source = Column(String, nullable=True)  # Source of vinegar mother
    inoculation_date = Column(DateTime, nullable=False)
    target_abv = Column(Numeric(5, 2), nullable=True)  # Target ABV for vinegar (8-13%)
    actual_abv = Column(Numeric(5, 2), nullable=True)  # Actual ABV achieved
    
    # Timing information
    planned_duration_days = Column(Integer, nullable=True)  # Planned duration in days
    actual_duration_days = Column(Numeric(5, 1), nullable=True)  # Actual duration in days
    completion_date = Column(DateTime, nullable=True)  # When the vinegar process was completed
    
    # Measurements
    initial_ph = Column(Numeric(4, 2), nullable=False)  # pH, 2 decimal places
    final_ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    acidity = Column(Numeric(5, 2), nullable=True)  # Acidity as percentage, 2 decimal places
    
    # Compound analysis
    esters_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    ketones_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    aldehydes_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    
    # Sensory evaluation
    aroma_notes = Column(Text, nullable=True)
    flavor_notes = Column(Text, nullable=True)
    clarity_rating = Column(Numeric(3, 1), nullable=True)  # 1-10 scale, 1 decimal place
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="vinegar_results")

class DistillationResults(Base):
    __tablename__ = "distillation_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    trial_number = Column(Integer, nullable=False)  # Which trial number this is (1 to total_trials)
    
    # Distillation parameters
    distillation_method = Column(String, nullable=False)  # e.g., "D1 Pot Distil", "D2 Reflux/Infuse"
    input_volume = Column(Numeric(10, 2), nullable=False)  # in milliliters, 2 decimal places
    output_volume = Column(Numeric(10, 2), nullable=True)  # in milliliters, 2 decimal places
    yield_percentage = Column(Numeric(5, 2), nullable=True)  # percentage, 2 decimal places
    
    # Quality tests
    abv = Column(Numeric(5, 2), nullable=True)  # alcohol by volume, 2 decimal places
    methanol_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    esters_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    vocs_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    
    # Expanded compound analysis
    vanillin_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    fusel_oils_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    turpines_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    ketones_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    aldehydes_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    glycerol_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    
    # Sample retention
    retained_raw_volume = Column(Numeric(10, 2), nullable=True)  # in milliliters, 2 decimal places
    retained_steep_volume = Column(Numeric(10, 2), nullable=True)  # in milliliters, 2 decimal places
    
    # Environmental reporting
    still_waste_volume = Column(Numeric(10, 2), nullable=True)  # in milliliters, 2 decimal places
    still_waste_analysis = Column(Text, nullable=True)  # Analysis of still waste
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="distillation_results")

class Stage2Results(Base):
    __tablename__ = "stage2_results"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    
    # Stage 2 parameters
    sdlc_results = Column(Text, nullable=True)  # SDLC analysis results
    megaquant_results = Column(Text, nullable=True)  # MegaQuant analysis results
    decision_criteria = Column(Text, nullable=True)  # Decision logic based on analysis
    
    # Measurements
    abv = Column(Numeric(5, 2), nullable=True)  # alcohol by volume, 2 decimal places
    ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    
    # Compound analysis
    vanillin_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    fusel_oils_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    turpines_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    ketones_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    aldehydes_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    esters_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    glycerol_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    vocs_content = Column(Numeric(5, 2), nullable=True)  # in mg/L, 2 decimal places
    
    # Sensory evaluation
    aroma_notes = Column(Text, nullable=True)
    flavor_notes = Column(Text, nullable=True)
    clarity_rating = Column(Numeric(3, 1), nullable=True)  # 1-10 scale, 1 decimal place
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="stage2_results")

class FruitPerformance(Base):
    __tablename__ = "fruit_performance"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("transformation_stages.id"))
    
    # Fruit performance metrics
    avg_gross_fruit_weight = Column(Numeric(8, 3), nullable=True)  # in kg, 3 decimal places
    juice_yield_per_gram = Column(Numeric(8, 4), nullable=True)  # milliliters per gram, 4 decimal places
    brix = Column(Numeric(5, 2), nullable=True)  # sugar content, 2 decimal places
    yan = Column(Numeric(5, 2), nullable=True)  # Yeast Assimilable Nitrogen, 2 decimal places
    ph = Column(Numeric(4, 2), nullable=True)  # pH, 2 decimal places
    starch_content = Column(Numeric(5, 2), nullable=True)  # in percentage, 2 decimal places
    
    # Sensory evaluation
    aroma_notes = Column(Text, nullable=True)
    flavor_notes = Column(Text, nullable=True)
    texture_notes = Column(Text, nullable=True)
    ripeness_rating = Column(Numeric(3, 1), nullable=True)  # 1-10 scale, 1 decimal place
    
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("TransformationStage", back_populates="fruit_performance") 