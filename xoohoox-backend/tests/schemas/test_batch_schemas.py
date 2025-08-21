import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.batch import (
    BatchCreate,
    BatchUpdate,
    BatchInDB,
    BatchWithRelations
)
from app.models.enums import (
    FruitType,
    AppleVariety,
    BatchStatus,
    FermentationStage,
    DistillationStage
)

def test_batch_create_validation():
    """Test BatchCreate schema validation."""
    # Valid data
    valid_data = {
        "fruit_type": FruitType.APPLE,
        "apple_variety": AppleVariety.GALA,
        "target_quantity": 1000.0,
        "status": BatchStatus.PLANNED,
        "notes": "Test batch"
    }
    batch = BatchCreate(**valid_data)
    assert batch.fruit_type == FruitType.APPLE
    assert batch.target_quantity == 1000.0

    # Invalid data - negative quantity
    invalid_data = valid_data.copy()
    invalid_data["target_quantity"] = -100.0
    with pytest.raises(ValidationError):
        BatchCreate(**invalid_data)

    # Invalid data - missing required field
    invalid_data = valid_data.copy()
    del invalid_data["fruit_type"]
    with pytest.raises(ValidationError):
        BatchCreate(**invalid_data)

def test_batch_update_validation():
    """Test BatchUpdate schema validation."""
    # Valid partial update
    valid_data = {
        "status": BatchStatus.IN_PROGRESS,
        "notes": "Updated notes"
    }
    batch = BatchUpdate(**valid_data)
    assert batch.status == BatchStatus.IN_PROGRESS
    assert batch.notes == "Updated notes"

    # Invalid status transition
    invalid_data = {
        "status": BatchStatus.COMPLETED,
        "fermentation_stage": FermentationStage.INITIAL
    }
    with pytest.raises(ValidationError):
        BatchUpdate(**invalid_data)

def test_batch_in_db_serialization():
    """Test BatchInDB schema serialization."""
    data = {
        "id": 1,
        "fruit_type": FruitType.APPLE,
        "apple_variety": AppleVariety.GALA,
        "target_quantity": 1000.0,
        "actual_quantity": 950.0,
        "status": BatchStatus.IN_PROGRESS,
        "fermentation_stage": FermentationStage.INITIAL,
        "distillation_stage": DistillationStage.NOT_STARTED,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "notes": "Test batch"
    }
    batch = BatchInDB(**data)
    assert batch.id == 1
    assert batch.fruit_type == FruitType.APPLE
    assert batch.actual_quantity == 950.0

def test_batch_with_relations_validation():
    """Test BatchWithRelations schema validation."""
    data = {
        "id": 1,
        "fruit_type": FruitType.APPLE,
        "apple_variety": AppleVariety.GALA,
        "target_quantity": 1000.0,
        "actual_quantity": 950.0,
        "status": BatchStatus.IN_PROGRESS,
        "fermentation_stage": FermentationStage.INITIAL,
        "distillation_stage": DistillationStage.NOT_STARTED,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "notes": "Test batch",
        "quality_checks": [],
        "maintenance_records": [],
        "environmental_impact": None
    }
    batch = BatchWithRelations(**data)
    assert batch.id == 1
    assert isinstance(batch.quality_checks, list)
    assert isinstance(batch.maintenance_records, list)
    assert batch.environmental_impact is None

def test_batch_custom_validators():
    """Test custom validators in batch schemas."""
    # Test quantity validator
    data = {
        "fruit_type": FruitType.APPLE,
        "apple_variety": AppleVariety.GALA,
        "target_quantity": 1000.0,
        "actual_quantity": 2000.0,  # Should be less than or equal to target
        "status": BatchStatus.IN_PROGRESS
    }
    with pytest.raises(ValidationError):
        BatchUpdate(**data)

    # Test status transition validator
    data = {
        "status": BatchStatus.COMPLETED,
        "fermentation_stage": FermentationStage.INITIAL,
        "distillation_stage": DistillationStage.NOT_STARTED
    }
    with pytest.raises(ValidationError):
        BatchUpdate(**data) 