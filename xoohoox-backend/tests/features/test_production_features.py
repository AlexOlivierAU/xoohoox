import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.chemistry import ChemistryAdjustment
from app.models.fermentation import FermentationKinetics
from app.models.distillation import DistillationLadder
from app.models.trial import Trial
from app.models.environmental import EnvironmentalImpact
from app.models.enums import (
    BatchStatus,
    FermentationStage,
    DistillationStage,
    TrialStatus,
    ChemistryParameter
)

@pytest.fixture
def test_batch(db: Session) -> Batch:
    """Create a test batch for feature testing."""
    batch = Batch(
        fruit_type="APPLE",
        apple_variety="GALA",
        target_quantity=1000.0,
        status=BatchStatus.IN_PROGRESS,
        fermentation_stage=FermentationStage.INITIAL,
        distillation_stage=DistillationStage.NOT_STARTED
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch

class TestChemistryAdjustment:
    """Test chemistry adjustment tracking features."""
    
    def test_add_adjustment(self, db: Session, test_batch: Batch):
        """Test adding a chemistry adjustment."""
        adjustment = ChemistryAdjustment(
            batch_id=test_batch.id,
            parameter=ChemistryParameter.PH,
            value=3.5,
            timestamp=datetime.now(),
            notes="Initial pH adjustment"
        )
        db.add(adjustment)
        db.commit()
        
        assert adjustment.id is not None
        assert adjustment.batch_id == test_batch.id
        assert adjustment.parameter == ChemistryParameter.PH
        assert adjustment.value == 3.5
    
    def test_adjustment_history(self, db: Session, test_batch: Batch):
        """Test retrieving adjustment history."""
        # Add multiple adjustments
        adjustments = [
            ChemistryAdjustment(
                batch_id=test_batch.id,
                parameter=ChemistryParameter.PH,
                value=3.5,
                timestamp=datetime.now() - timedelta(hours=2)
            ),
            ChemistryAdjustment(
                batch_id=test_batch.id,
                parameter=ChemistryParameter.PH,
                value=3.7,
                timestamp=datetime.now() - timedelta(hours=1)
            )
        ]
        for adj in adjustments:
            db.add(adj)
        db.commit()
        
        history = db.query(ChemistryAdjustment).filter(
            ChemistryAdjustment.batch_id == test_batch.id
        ).order_by(ChemistryAdjustment.timestamp).all()
        
        assert len(history) == 2
        assert history[0].value == 3.5
        assert history[1].value == 3.7

class TestFermentationKinetics:
    """Test fermentation kinetics monitoring."""
    
    def test_add_kinetics_data(self, db: Session, test_batch: Batch):
        """Test adding fermentation kinetics data."""
        kinetics = FermentationKinetics(
            batch_id=test_batch.id,
            timestamp=datetime.now(),
            temperature=25.5,
            specific_gravity=1.050,
            brix=12.5,
            ph=3.6,
            notes="Initial fermentation readings"
        )
        db.add(kinetics)
        db.commit()
        
        assert kinetics.id is not None
        assert kinetics.batch_id == test_batch.id
        assert kinetics.temperature == 25.5
        assert kinetics.specific_gravity == 1.050
    
    def test_kinetics_trend_analysis(self, db: Session, test_batch: Batch):
        """Test analyzing fermentation kinetics trends."""
        # Add multiple readings
        readings = [
            FermentationKinetics(
                batch_id=test_batch.id,
                timestamp=datetime.now() - timedelta(hours=2),
                temperature=25.0,
                specific_gravity=1.060,
                brix=13.0,
                ph=3.5
            ),
            FermentationKinetics(
                batch_id=test_batch.id,
                timestamp=datetime.now() - timedelta(hours=1),
                temperature=25.5,
                specific_gravity=1.055,
                brix=12.8,
                ph=3.6
            )
        ]
        for reading in readings:
            db.add(reading)
        db.commit()
        
        trend = db.query(FermentationKinetics).filter(
            FermentationKinetics.batch_id == test_batch.id
        ).order_by(FermentationKinetics.timestamp).all()
        
        assert len(trend) == 2
        assert trend[0].specific_gravity > trend[1].specific_gravity  # Should decrease
        assert trend[0].temperature < trend[1].temperature  # Should increase

class TestDistillationLadder:
    """Test distillation ladder progression."""
    
    def test_add_ladder_step(self, db: Session, test_batch: Batch):
        """Test adding a distillation ladder step."""
        step = DistillationLadder(
            batch_id=test_batch.id,
            step_number=1,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=2),
            temperature=78.5,
            abv=40.0,
            volume=100.0,
            notes="First distillation run"
        )
        db.add(step)
        db.commit()
        
        assert step.id is not None
        assert step.batch_id == test_batch.id
        assert step.step_number == 1
        assert step.abv == 40.0
    
    def test_ladder_progression(self, db: Session, test_batch: Batch):
        """Test distillation ladder progression."""
        # Add multiple steps
        steps = [
            DistillationLadder(
                batch_id=test_batch.id,
                step_number=1,
                start_time=datetime.now() - timedelta(hours=4),
                end_time=datetime.now() - timedelta(hours=2),
                temperature=78.5,
                abv=40.0,
                volume=100.0
            ),
            DistillationLadder(
                batch_id=test_batch.id,
                step_number=2,
                start_time=datetime.now() - timedelta(hours=2),
                end_time=datetime.now(),
                temperature=79.0,
                abv=60.0,
                volume=50.0
            )
        ]
        for step in steps:
            db.add(step)
        db.commit()
        
        progression = db.query(DistillationLadder).filter(
            DistillationLadder.batch_id == test_batch.id
        ).order_by(DistillationLadder.step_number).all()
        
        assert len(progression) == 2
        assert progression[0].abv < progression[1].abv  # ABV should increase
        assert progression[0].volume > progression[1].volume  # Volume should decrease

class TestTrialManagement:
    """Test trial management features."""
    
    def test_create_trial(self, db: Session, test_batch: Batch):
        """Test creating a new trial."""
        trial = Trial(
            batch_id=test_batch.id,
            name="Test Trial 1",
            description="Testing new fermentation parameters",
            status=TrialStatus.IN_PROGRESS,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7),
            parameters={
                "temperature": 25.5,
                "ph": 3.6,
                "yeast_strain": "Saccharomyces cerevisiae"
            }
        )
        db.add(trial)
        db.commit()
        
        assert trial.id is not None
        assert trial.batch_id == test_batch.id
        assert trial.status == TrialStatus.IN_PROGRESS
        assert "temperature" in trial.parameters
    
    def test_trial_results(self, db: Session, test_batch: Batch):
        """Test recording trial results."""
        trial = Trial(
            batch_id=test_batch.id,
            name="Test Trial 1",
            status=TrialStatus.COMPLETED,
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now(),
            parameters={"temperature": 25.5},
            results={
                "final_abv": 40.0,
                "yield": 85.0,
                "quality_score": 8.5
            }
        )
        db.add(trial)
        db.commit()
        
        assert trial.results["final_abv"] == 40.0
        assert trial.results["yield"] == 85.0
        assert trial.status == TrialStatus.COMPLETED

class TestEnvironmentalImpact:
    """Test environmental impact tracking."""
    
    def test_add_impact_data(self, db: Session, test_batch: Batch):
        """Test adding environmental impact data."""
        impact = EnvironmentalImpact(
            batch_id=test_batch.id,
            timestamp=datetime.now(),
            water_usage=1000.0,  # liters
            energy_usage=50.0,   # kWh
            waste_generated=10.0, # kg
            notes="Initial environmental impact measurement"
        )
        db.add(impact)
        db.commit()
        
        assert impact.id is not None
        assert impact.batch_id == test_batch.id
        assert impact.water_usage == 1000.0
        assert impact.energy_usage == 50.0
    
    def test_impact_tracking(self, db: Session, test_batch: Batch):
        """Test tracking environmental impact over time."""
        # Add multiple measurements
        measurements = [
            EnvironmentalImpact(
                batch_id=test_batch.id,
                timestamp=datetime.now() - timedelta(hours=2),
                water_usage=1000.0,
                energy_usage=50.0,
                waste_generated=10.0
            ),
            EnvironmentalImpact(
                batch_id=test_batch.id,
                timestamp=datetime.now() - timedelta(hours=1),
                water_usage=1500.0,
                energy_usage=75.0,
                waste_generated=15.0
            )
        ]
        for measurement in measurements:
            db.add(measurement)
        db.commit()
        
        tracking = db.query(EnvironmentalImpact).filter(
            EnvironmentalImpact.batch_id == test_batch.id
        ).order_by(EnvironmentalImpact.timestamp).all()
        
        assert len(tracking) == 2
        assert tracking[0].water_usage < tracking[1].water_usage
        assert tracking[0].energy_usage < tracking[1].energy_usage
        assert tracking[0].waste_generated < tracking[1].waste_generated 