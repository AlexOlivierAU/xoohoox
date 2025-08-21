import pytest
from datetime import datetime
from app.models.juicing_input_log import JuicingInputLog
from app.models.enums import FruitType

def test_juicing_input_creation():
    """Test creating a juicing input log with valid data."""
    input_date = datetime.utcnow()
    juicing_input = JuicingInputLog(
        batch_id=1,
        fruit_type=FruitType.APPLE,
        input_quantity=500.0,
        input_date=input_date,
        operator_id=1,
        equipment_id=1,
        notes="First batch of the day"
    )
    
    assert juicing_input.batch_id == 1
    assert juicing_input.fruit_type == FruitType.APPLE
    assert juicing_input.input_quantity == 500.0
    assert juicing_input.input_date == input_date
    assert juicing_input.operator_id == 1
    assert juicing_input.equipment_id == 1
    assert juicing_input.notes == "First batch of the day"

def test_juicing_input_defaults():
    """Test default values for juicing input fields."""
    juicing_input = JuicingInputLog(
        batch_id=1,
        fruit_type=FruitType.APPLE,
        input_quantity=500.0,
        operator_id=1,
        equipment_id=1
    )
    
    assert isinstance(juicing_input.input_date, datetime)  # Should default to current time
    assert juicing_input.notes is None

def test_juicing_input_representation():
    """Test string representation of JuicingInputLog model."""
    juicing_input = JuicingInputLog(
        batch_id=1,
        fruit_type=FruitType.APPLE,
        input_quantity=500.0,
        operator_id=1,
        equipment_id=1
    )
    
    str_repr = str(juicing_input)
    assert "JuicingInputLog" in str_repr
    assert "APPLE" in str_repr
    assert "500.0" in str_repr

def test_juicing_input_to_dict():
    """Test the to_dict method of JuicingInputLog model."""
    input_date = datetime.utcnow()
    juicing_input = JuicingInputLog(
        batch_id=1,
        fruit_type=FruitType.APPLE,
        input_quantity=500.0,
        input_date=input_date,
        operator_id=1,
        equipment_id=1,
        notes="First batch of the day"
    )
    
    input_dict = juicing_input.to_dict()
    
    assert input_dict['batch_id'] == 1
    assert input_dict['fruit_type'] == FruitType.APPLE.value
    assert input_dict['input_quantity'] == 500.0
    assert 'input_date' in input_dict
    assert input_dict['operator_id'] == 1
    assert input_dict['equipment_id'] == 1
    assert input_dict['notes'] == "First batch of the day"

def test_juicing_input_validation():
    """Test juicing input validation rules."""
    # Test invalid input quantity (negative)
    with pytest.raises(ValueError):
        JuicingInputLog(
            batch_id=1,
            fruit_type=FruitType.APPLE,
            input_quantity=-100.0,  # Negative quantity
            operator_id=1,
            equipment_id=1
        )
    
    # Test invalid input quantity (zero)
    with pytest.raises(ValueError):
        JuicingInputLog(
            batch_id=1,
            fruit_type=FruitType.APPLE,
            input_quantity=0.0,  # Zero quantity
            operator_id=1,
            equipment_id=1
        )

def test_juicing_input_batch_tracking():
    """Test juicing input relationship with batch tracking."""
    juicing_input = JuicingInputLog(
        batch_id=1,
        fruit_type=FruitType.APPLE,
        input_quantity=500.0,
        operator_id=1,
        equipment_id=1
    )
    
    # Test that the input is associated with the correct batch
    assert juicing_input.batch_id == 1
    
    # Test that the fruit type matches the batch's fruit type
    assert juicing_input.fruit_type == FruitType.APPLE

def test_juicing_input_equipment_tracking():
    """Test juicing input relationship with equipment."""
    juicing_input = JuicingInputLog(
        batch_id=1,
        fruit_type=FruitType.APPLE,
        input_quantity=500.0,
        operator_id=1,
        equipment_id=1
    )
    
    # Test that the input is associated with the correct equipment
    assert juicing_input.equipment_id == 1
    
    # Test that the operator is recorded
    assert juicing_input.operator_id == 1 