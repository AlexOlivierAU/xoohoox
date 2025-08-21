import pytest
from datetime import datetime, timedelta
from app.models.batch_tracking import BatchTracking
from app.models.enums import BatchStatus, FruitType

def test_batch_creation():
    """Test creating a batch with valid data."""
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        status=BatchStatus.PLANNED,
        target_quantity=1000.0,
        production_date=datetime.utcnow(),
        recipe_id=1
    )
    
    assert batch.batch_number == "B001"
    assert batch.fruit_type == FruitType.APPLE
    assert batch.status == BatchStatus.PLANNED
    assert batch.target_quantity == 1000.0
    assert isinstance(batch.production_date, datetime)
    assert batch.recipe_id == 1

def test_batch_defaults():
    """Test default values for batch fields."""
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        target_quantity=1000.0,
        recipe_id=1
    )
    
    assert batch.status == BatchStatus.PLANNED  # Should default to PLANNED
    assert batch.final_product_quantity is None
    assert batch.processing_end_date is None
    assert batch.notes is None

def test_batch_status_transitions():
    """Test batch status transitions."""
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        target_quantity=1000.0,
        recipe_id=1
    )
    
    # Test valid status transitions
    batch.status = BatchStatus.IN_PROGRESS
    assert batch.status == BatchStatus.IN_PROGRESS
    
    batch.status = BatchStatus.COMPLETED
    assert batch.status == BatchStatus.COMPLETED
    
    # Test setting final values when completed
    batch.final_product_quantity = 950.0
    batch.processing_end_date = datetime.utcnow()
    assert batch.final_product_quantity == 950.0
    assert isinstance(batch.processing_end_date, datetime)

def test_batch_representation():
    """Test string representation of BatchTracking model."""
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        target_quantity=1000.0,
        recipe_id=1
    )
    
    str_repr = str(batch)
    assert "BatchTracking" in str_repr
    assert "B001" in str_repr

def test_batch_to_dict():
    """Test the to_dict method of BatchTracking model."""
    production_date = datetime.utcnow()
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        status=BatchStatus.PLANNED,
        target_quantity=1000.0,
        production_date=production_date,
        recipe_id=1
    )
    
    batch_dict = batch.to_dict()
    
    assert batch_dict['batch_number'] == "B001"
    assert batch_dict['fruit_type'] == FruitType.APPLE.value
    assert batch_dict['status'] == BatchStatus.PLANNED.value
    assert batch_dict['target_quantity'] == 1000.0
    assert 'production_date' in batch_dict
    assert batch_dict['recipe_id'] == 1

def test_batch_validation():
    """Test batch validation rules."""
    # Test invalid target quantity
    with pytest.raises(ValueError):
        BatchTracking(
            batch_number="B001",
            fruit_type=FruitType.APPLE,
            target_quantity=-100.0,  # Negative quantity
            recipe_id=1
        )
    
    # Test invalid final product quantity
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        target_quantity=1000.0,
        recipe_id=1
    )
    with pytest.raises(ValueError):
        batch.final_product_quantity = -50.0  # Negative quantity

def test_batch_dates_validation():
    """Test batch dates validation."""
    production_date = datetime.utcnow()
    processing_end_date = production_date - timedelta(days=1)  # End date before production date
    
    batch = BatchTracking(
        batch_number="B001",
        fruit_type=FruitType.APPLE,
        target_quantity=1000.0,
        production_date=production_date,
        recipe_id=1
    )
    
    # Test setting invalid processing end date
    with pytest.raises(ValueError):
        batch.processing_end_date = processing_end_date 