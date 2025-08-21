from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, condecimal

from app.models.transformation import TransformationType, ProcessStatus, JuiceProcessingType

# Transformation Stage schemas
class TransformationStageBase(BaseModel):
    batch_id: int
    stage_number: int
    stage_name: str
    stage_type: str
    status: str
    total_trials: int = 1
    trials_to_proceed: Optional[int] = None
    parent_stage_id: Optional[int] = None
    upscale_factor: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    target_volume: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    planned_duration_days: Optional[int] = None
    actual_duration_days: Optional[condecimal(max_digits=5, decimal_places=1)] = None
    branching_rule: Optional[str] = None  # For vinegar path (8-13% ABV) or other branching logic

class TransformationStageCreate(TransformationStageBase):
    created_by: str
    updated_by: str

class TransformationStageUpdate(TransformationStageBase):
    pass

class TransformationStage(TransformationStageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Juicing Results schemas
class JuicingResultsBase(BaseModel):
    stage_id: int
    
    # Juice processing variant
    juice_processing_type: str
    is_raw_juice_ferment: bool = False  # For JP1 (one-time only rule)
    
    # Input measurements
    input_weight: Optional[condecimal(max_digits=10, decimal_places=3)] = None
    fruit_condition: Optional[str] = None
    
    # Output measurements
    juice_volume: condecimal(max_digits=10, decimal_places=2)
    juice_yield: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    juice_yield_per_gram: Optional[condecimal(max_digits=8, decimal_places=4)] = None
    brix: condecimal(max_digits=5, decimal_places=2)
    ph: condecimal(max_digits=4, decimal_places=2)
    temperature: condecimal(max_digits=5, decimal_places=2)
    
    # Process parameters
    press_pressure: Optional[condecimal(max_digits=6, decimal_places=2)] = None
    press_time: Optional[condecimal(max_digits=8, decimal_places=2)] = None
    maceration_time: Optional[condecimal(max_digits=8, decimal_places=2)] = None
    extraction_method: Optional[str] = None
    
    notes: Optional[str] = None

class JuicingResultsCreate(JuicingResultsBase):
    created_by: str
    updated_by: str

class JuicingResultsUpdate(JuicingResultsBase):
    pass

class JuicingResults(JuicingResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Chemistry Results schemas
class ChemistryResultsBase(BaseModel):
    stage_id: int
    
    # Initial readings
    initial_ph: condecimal(max_digits=4, decimal_places=2)
    initial_sg: condecimal(max_digits=5, decimal_places=4)
    
    # Adjustments
    sodium_bicarb_added: Optional[condecimal(max_digits=6, decimal_places=2)] = None
    reaction_time_hours: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Target values
    target_ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    target_sg: Optional[condecimal(max_digits=5, decimal_places=4)] = None
    
    # Final readings
    final_ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    final_sg: Optional[condecimal(max_digits=5, decimal_places=4)] = None
    
    # Process parameters
    batch_size: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    scale_up_notes: Optional[str] = None
    no_adjustments_allowed: bool = False  # For raw juice ferments (JP1)
    
    notes: Optional[str] = None

class ChemistryResultsCreate(ChemistryResultsBase):
    pass

class ChemistryResultsUpdate(ChemistryResultsBase):
    pass

class ChemistryResults(ChemistryResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Heat Activation Results schemas
class HeatActivationResultsBase(BaseModel):
    stage_id: int
    
    # Heat activation parameters
    target_temperature: condecimal(max_digits=5, decimal_places=2)
    actual_temperature: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    rest_time_hours: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Nutrient and yeast preparation
    nutrient_concentration: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    yeast_concentration: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    rest_time_minutes: Optional[int] = None
    
    # Pitch conditions
    pitch_temperature: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    pitch_ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    pitch_sg: Optional[condecimal(max_digits=5, decimal_places=4)] = None
    
    notes: Optional[str] = None

class HeatActivationResultsCreate(HeatActivationResultsBase):
    pass

class HeatActivationResultsUpdate(HeatActivationResultsBase):
    pass

class HeatActivationResults(HeatActivationResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Fermentation Results schemas
class FermentationResultsBase(BaseModel):
    stage_id: int
    trial_number: int
    proceeds_to_next_stage: bool = False
    parent_trial_id: Optional[int] = None
    upscale_batch: Optional[str] = None
    
    # Yeast information
    yeast_strain: str
    inoculation_date: datetime
    yeast_source: Optional[str] = None
    
    # Timing information
    planned_duration_days: Optional[int] = None
    actual_duration_days: Optional[condecimal(max_digits=5, decimal_places=1)] = None
    completion_date: Optional[datetime] = None
    lag_time_hours: Optional[condecimal(max_digits=5, decimal_places=1)] = None
    active_fermentation_days: Optional[condecimal(max_digits=5, decimal_places=1)] = None
    
    # Fermentation timing factors
    temperature_control_method: Optional[str] = None
    temperature_variance: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    nutrient_additions: Optional[str] = None
    aeration_frequency: Optional[str] = None
    stuck_fermentation: bool = False
    stuck_fermentation_resolution: Optional[str] = None
    restart_attempts: Optional[int] = None
    
    # Initial measurements
    initial_volume: condecimal(max_digits=10, decimal_places=2)
    initial_gravity: condecimal(max_digits=5, decimal_places=4)
    initial_ph: condecimal(max_digits=4, decimal_places=2)
    initial_temperature: condecimal(max_digits=5, decimal_places=2)
    
    # Ongoing measurements
    current_gravity: Optional[condecimal(max_digits=5, decimal_places=4)] = None
    current_ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    current_temperature: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Final measurements
    final_gravity: Optional[condecimal(max_digits=5, decimal_places=4)] = None
    final_ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    alcohol_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Sensory evaluation
    aroma_notes: Optional[str] = None
    flavor_notes: Optional[str] = None
    clarity_rating: Optional[condecimal(max_digits=3, decimal_places=1)] = None
    
    # Trial selection criteria
    selection_score: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    selection_notes: Optional[str] = None
    
    # Upscale specific fields
    upscale_volume: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    upscale_ratio: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    upscale_notes: Optional[str] = None
    
    notes: Optional[str] = None

class FermentationResultsCreate(FermentationResultsBase):
    created_by: str
    updated_by: str

class FermentationResultsUpdate(FermentationResultsBase):
    pass

class FermentationResults(FermentationResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Vinegar Results schemas
class VinegarResultsBase(BaseModel):
    stage_id: int
    
    # Vinegar processing parameters
    vinegar_mother_source: Optional[str] = None
    inoculation_date: datetime
    target_abv: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    actual_abv: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Timing information
    planned_duration_days: Optional[int] = None
    actual_duration_days: Optional[condecimal(max_digits=5, decimal_places=1)] = None
    completion_date: Optional[datetime] = None
    
    # Measurements
    initial_ph: condecimal(max_digits=4, decimal_places=2)
    final_ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    acidity: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Compound analysis
    esters_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    ketones_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    aldehydes_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Sensory evaluation
    aroma_notes: Optional[str] = None
    flavor_notes: Optional[str] = None
    clarity_rating: Optional[condecimal(max_digits=3, decimal_places=1)] = None
    
    notes: Optional[str] = None

class VinegarResultsCreate(VinegarResultsBase):
    pass

class VinegarResultsUpdate(VinegarResultsBase):
    pass

class VinegarResults(VinegarResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Distillation Results schemas
class DistillationResultsBase(BaseModel):
    stage_id: int
    trial_number: int
    
    # Distillation parameters
    distillation_method: str
    input_volume: condecimal(max_digits=10, decimal_places=2)
    output_volume: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    yield_percentage: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Quality tests
    abv: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    methanol_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    esters_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    vocs_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Expanded compound analysis
    vanillin_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    fusel_oils_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    turpines_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    ketones_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    aldehydes_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    glycerol_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Sample retention
    retained_raw_volume: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    retained_steep_volume: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    
    # Environmental reporting
    still_waste_volume: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    still_waste_analysis: Optional[str] = None
    
    notes: Optional[str] = None

class DistillationResultsCreate(DistillationResultsBase):
    pass

class DistillationResultsUpdate(DistillationResultsBase):
    pass

class DistillationResults(DistillationResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Stage 2 Results schemas
class Stage2ResultsBase(BaseModel):
    stage_id: int
    
    # Stage 2 parameters
    sdlc_results: Optional[str] = None
    megaquant_results: Optional[str] = None
    decision_criteria: Optional[str] = None
    
    # Measurements
    abv: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    
    # Compound analysis
    vanillin_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    fusel_oils_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    turpines_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    ketones_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    aldehydes_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    esters_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    glycerol_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    vocs_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Sensory evaluation
    aroma_notes: Optional[str] = None
    flavor_notes: Optional[str] = None
    clarity_rating: Optional[condecimal(max_digits=3, decimal_places=1)] = None
    
    notes: Optional[str] = None

class Stage2ResultsCreate(Stage2ResultsBase):
    pass

class Stage2ResultsUpdate(Stage2ResultsBase):
    pass

class Stage2Results(Stage2ResultsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Fruit Performance schemas
class FruitPerformanceBase(BaseModel):
    stage_id: int
    
    # Fruit performance metrics
    avg_gross_fruit_weight: Optional[condecimal(max_digits=8, decimal_places=3)] = None
    juice_yield_per_gram: Optional[condecimal(max_digits=8, decimal_places=4)] = None
    brix: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    yan: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    ph: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    starch_content: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    
    # Sensory evaluation
    aroma_notes: Optional[str] = None
    flavor_notes: Optional[str] = None
    texture_notes: Optional[str] = None
    ripeness_rating: Optional[condecimal(max_digits=3, decimal_places=1)] = None
    
    notes: Optional[str] = None

class FruitPerformanceCreate(FruitPerformanceBase):
    pass

class FruitPerformanceUpdate(FruitPerformanceBase):
    pass

class FruitPerformance(FruitPerformanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Combined schema for transformation stage with results
class TransformationStageWithResults(TransformationStage):
    juicing_results: Optional[JuicingResults] = None
    chemistry_results: Optional[ChemistryResults] = None
    heat_activation_results: Optional[HeatActivationResults] = None
    fermentation_results: Optional[FermentationResults] = None
    vinegar_results: Optional[VinegarResults] = None
    distillation_results: Optional[DistillationResults] = None
    stage2_results: Optional[Stage2Results] = None
    fruit_performance: Optional[FruitPerformance] = None
    upscale_stages: List["TransformationStageWithResults"] = []

    class Config:
        from_attributes = True

# For nested relationships
TransformationStageWithResults.model_rebuild() 