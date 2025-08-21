from datetime import datetime, timedelta
import pytest
from pydantic import ValidationError

from app.schemas.transformation import (
    TransformationCreate,
    TransformationType,
    TransformationStatus,
)

def test_valid_transformation():
    now = datetime.now()
    
    test_data = {
        "transformation_id": "TRANS-001",
        "batch_id": "BATCH-001",
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "status": TransformationStatus.IN_PROGRESS,
        "parameters": {
            "temperature": 25.0,
            "humidity": 60.0,
            "duration_hours": 48
        },
        "notes": "Standard fermentation process",
        "operator": "fermentation_specialist",
        "supervisor": "quality_manager"
    }
    
    transformation = TransformationCreate(**test_data)
    assert transformation.transformation_id == "TRANS-001"
    assert transformation.batch_id == "BATCH-001"
    assert transformation.type == TransformationType.FERMENTATION
    assert transformation.status == TransformationStatus.IN_PROGRESS

def test_invalid_transformation_id():
    now = datetime.now()
    
    test_data = {
        "transformation_id": "",  # Invalid: empty transformation ID
        "batch_id": "BATCH-001",
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "status": TransformationStatus.IN_PROGRESS,
        "parameters": {
            "temperature": 25.0,
            "humidity": 60.0,
            "duration_hours": 48
        },
        "notes": "Standard fermentation process",
        "operator": "fermentation_specialist",
        "supervisor": "quality_manager"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        TransformationCreate(**test_data)
    assert "Transformation ID cannot be empty" in str(exc_info.value)

def test_invalid_batch_id():
    now = datetime.now()
    
    test_data = {
        "transformation_id": "TRANS-002",
        "batch_id": "",  # Invalid: empty batch ID
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "status": TransformationStatus.IN_PROGRESS,
        "parameters": {
            "temperature": 25.0,
            "humidity": 60.0,
            "duration_hours": 48
        },
        "notes": "Standard fermentation process",
        "operator": "fermentation_specialist",
        "supervisor": "quality_manager"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        TransformationCreate(**test_data)
    assert "Batch ID cannot be empty" in str(exc_info.value)

def test_invalid_temperature():
    now = datetime.now()
    
    test_data = {
        "transformation_id": "TRANS-003",
        "batch_id": "BATCH-001",
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "status": TransformationStatus.IN_PROGRESS,
        "parameters": {
            "temperature": 150.0,  # Invalid: temperature too high
            "humidity": 60.0,
            "duration_hours": 48
        },
        "notes": "Standard fermentation process",
        "operator": "fermentation_specialist",
        "supervisor": "quality_manager"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        TransformationCreate(**test_data)
    assert "Temperature must be between 0 and 100 degrees Celsius" in str(exc_info.value)

def test_invalid_duration():
    now = datetime.now()
    
    test_data = {
        "transformation_id": "TRANS-004",
        "batch_id": "BATCH-001",
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "status": TransformationStatus.IN_PROGRESS,
        "parameters": {
            "temperature": 25.0,
            "humidity": 60.0,
            "duration_hours": -48  # Invalid: negative duration
        },
        "notes": "Standard fermentation process",
        "operator": "fermentation_specialist",
        "supervisor": "quality_manager"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        TransformationCreate(**test_data)
    assert "Duration must be positive" in str(exc_info.value)

def test_invalid_operator():
    now = datetime.now()
    
    test_data = {
        "transformation_id": "TRANS-005",
        "batch_id": "BATCH-001",
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "status": TransformationStatus.IN_PROGRESS,
        "parameters": {
            "temperature": 25.0,
            "humidity": 60.0,
            "duration_hours": 48
        },
        "notes": "Standard fermentation process",
        "operator": "",  # Invalid: empty operator
        "supervisor": "quality_manager"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        TransformationCreate(**test_data)
    assert "Operator cannot be empty" in str(exc_info.value)

def test_completed_transformation():
    now = datetime.now()
    end_date = now + timedelta(hours=48)
    
    test_data = {
        "transformation_id": "TRANS-006",
        "batch_id": "BATCH-001",
        "type": TransformationType.FERMENTATION,
        "start_date": now,
        "end_date": end_date,
        "status": TransformationStatus.COMPLETED,
        "parameters": {
            "temperature": 25.0,
            "humidity": 60.0,
            "duration_hours": 48
        },
        "notes": "Completed fermentation process",
        "operator": "fermentation_specialist",
        "supervisor": "quality_manager",
        "completion_notes": "Process completed successfully"
    }
    
    transformation = TransformationCreate(**test_data)
    assert transformation.status == TransformationStatus.COMPLETED
    assert transformation.end_date is not None
    assert transformation.completion_notes is not None 