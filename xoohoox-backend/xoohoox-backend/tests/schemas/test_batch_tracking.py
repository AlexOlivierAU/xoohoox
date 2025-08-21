from datetime import datetime, timedelta
import pytest
from pydantic import ValidationError

from app.schemas.batch_tracking import (
    BatchCreate,
    BatchStatus,
    BatchType,
    BatchPriority,
)

def test_valid_batch():
    now = datetime.now()
    
    test_data = {
        "batch_id": "BATCH-001",
        "type": BatchType.JUICE,
        "status": BatchStatus.PENDING,
        "priority": BatchPriority.MEDIUM,
        "start_date": now,
        "expected_completion_date": now + timedelta(days=7),
        "description": "Standard juice production batch",
        "operator": "production_operator",
        "recipe_id": "RECIPE-001",
        "target_volume_liters": 1000,
        "notes": "Regular production batch"
    }
    
    batch = BatchCreate(**test_data)
    assert batch.batch_id == "BATCH-001"
    assert batch.type == BatchType.JUICE
    assert batch.status == BatchStatus.PENDING
    assert batch.priority == BatchPriority.MEDIUM

def test_invalid_batch_id():
    now = datetime.now()
    
    test_data = {
        "batch_id": "",  # Invalid: empty batch ID
        "type": BatchType.JUICE,
        "status": BatchStatus.PENDING,
        "priority": BatchPriority.MEDIUM,
        "start_date": now,
        "expected_completion_date": now + timedelta(days=7),
        "description": "Standard juice production batch",
        "operator": "production_operator",
        "recipe_id": "RECIPE-001",
        "target_volume_liters": 1000,
        "notes": "Regular production batch"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BatchCreate(**test_data)
    assert "Batch ID cannot be empty" in str(exc_info.value)

def test_invalid_recipe_id():
    now = datetime.now()
    
    test_data = {
        "batch_id": "BATCH-002",
        "type": BatchType.JUICE,
        "status": BatchStatus.PENDING,
        "priority": BatchPriority.MEDIUM,
        "start_date": now,
        "expected_completion_date": now + timedelta(days=7),
        "description": "Standard juice production batch",
        "operator": "production_operator",
        "recipe_id": "",  # Invalid: empty recipe ID
        "target_volume_liters": 1000,
        "notes": "Regular production batch"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BatchCreate(**test_data)
    assert "Recipe ID cannot be empty" in str(exc_info.value)

def test_invalid_completion_date():
    now = datetime.now()
    
    test_data = {
        "batch_id": "BATCH-003",
        "type": BatchType.JUICE,
        "status": BatchStatus.PENDING,
        "priority": BatchPriority.MEDIUM,
        "start_date": now,
        "expected_completion_date": now - timedelta(days=1),  # Invalid: past date
        "description": "Standard juice production batch",
        "operator": "production_operator",
        "recipe_id": "RECIPE-001",
        "target_volume_liters": 1000,
        "notes": "Regular production batch"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BatchCreate(**test_data)
    assert "Expected completion date cannot be in the past" in str(exc_info.value)

def test_invalid_volume():
    now = datetime.now()
    
    test_data = {
        "batch_id": "BATCH-004",
        "type": BatchType.JUICE,
        "status": BatchStatus.PENDING,
        "priority": BatchPriority.MEDIUM,
        "start_date": now,
        "expected_completion_date": now + timedelta(days=7),
        "description": "Standard juice production batch",
        "operator": "production_operator",
        "recipe_id": "RECIPE-001",
        "target_volume_liters": -1000,  # Invalid: negative volume
        "notes": "Regular production batch"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BatchCreate(**test_data)
    assert "Target volume must be positive" in str(exc_info.value)

def test_invalid_operator():
    now = datetime.now()
    
    test_data = {
        "batch_id": "BATCH-005",
        "type": BatchType.JUICE,
        "status": BatchStatus.PENDING,
        "priority": BatchPriority.MEDIUM,
        "start_date": now,
        "expected_completion_date": now + timedelta(days=7),
        "description": "Standard juice production batch",
        "operator": "",  # Invalid: empty operator
        "recipe_id": "RECIPE-001",
        "target_volume_liters": 1000,
        "notes": "Regular production batch"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BatchCreate(**test_data)
    assert "Operator cannot be empty" in str(exc_info.value)

def test_completed_batch():
    now = datetime.now()
    completion_date = now - timedelta(hours=2)
    
    test_data = {
        "batch_id": "BATCH-006",
        "type": BatchType.JUICE,
        "status": BatchStatus.COMPLETED,
        "priority": BatchPriority.MEDIUM,
        "start_date": now - timedelta(days=1),
        "expected_completion_date": now - timedelta(days=1),
        "completion_date": completion_date,
        "description": "Standard juice production batch",
        "operator": "production_operator",
        "recipe_id": "RECIPE-001",
        "target_volume_liters": 1000,
        "actual_volume_liters": 980,
        "notes": "Batch completed successfully",
        "completion_notes": "All quality checks passed"
    }
    
    batch = BatchCreate(**test_data)
    assert batch.status == BatchStatus.COMPLETED
    assert batch.completion_date is not None
    assert batch.actual_volume_liters is not None
    assert batch.completion_notes is not None 