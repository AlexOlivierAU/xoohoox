from datetime import datetime, timedelta
import pytest
from pydantic import ValidationError

from app.schemas.equipment_maintenance import (
    MaintenanceRecordCreate,
    MaintenanceType,
    MaintenanceStatus,
    MaintenancePriority,
)

def test_valid_maintenance_record():
    now = datetime.now()
    
    test_data = {
        "record_id": "MNT-001",
        "equipment_id": "EQ-001",
        "maintenance_type": MaintenanceType.PREVENTIVE,
        "scheduled_date": now + timedelta(days=7),
        "status": MaintenanceStatus.SCHEDULED,
        "priority": MaintenancePriority.MEDIUM,
        "description": "Regular maintenance check",
        "technician": "maintenance_tech",
        "estimated_duration": 120,  # minutes
        "parts_required": ["filter", "lubricant"],
        "notes": "Standard maintenance procedure"
    }
    
    record = MaintenanceRecordCreate(**test_data)
    assert record.record_id == "MNT-001"
    assert record.equipment_id == "EQ-001"
    assert record.maintenance_type == MaintenanceType.PREVENTIVE
    assert record.status == MaintenanceStatus.SCHEDULED
    assert record.priority == MaintenancePriority.MEDIUM

def test_invalid_record_id():
    now = datetime.now()
    
    test_data = {
        "record_id": "",  # Invalid: empty record ID
        "equipment_id": "EQ-001",
        "maintenance_type": MaintenanceType.PREVENTIVE,
        "scheduled_date": now + timedelta(days=7),
        "status": MaintenanceStatus.SCHEDULED,
        "priority": MaintenancePriority.MEDIUM,
        "description": "Regular maintenance check",
        "technician": "maintenance_tech",
        "estimated_duration": 120,
        "parts_required": ["filter", "lubricant"],
        "notes": "Standard maintenance procedure"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MaintenanceRecordCreate(**test_data)
    assert "Record ID cannot be empty" in str(exc_info.value)

def test_invalid_equipment_id():
    now = datetime.now()
    
    test_data = {
        "record_id": "MNT-002",
        "equipment_id": "",  # Invalid: empty equipment ID
        "maintenance_type": MaintenanceType.PREVENTIVE,
        "scheduled_date": now + timedelta(days=7),
        "status": MaintenanceStatus.SCHEDULED,
        "priority": MaintenancePriority.MEDIUM,
        "description": "Regular maintenance check",
        "technician": "maintenance_tech",
        "estimated_duration": 120,
        "parts_required": ["filter", "lubricant"],
        "notes": "Standard maintenance procedure"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MaintenanceRecordCreate(**test_data)
    assert "Equipment ID cannot be empty" in str(exc_info.value)

def test_invalid_scheduled_date():
    now = datetime.now()
    
    test_data = {
        "record_id": "MNT-003",
        "equipment_id": "EQ-001",
        "maintenance_type": MaintenanceType.PREVENTIVE,
        "scheduled_date": now - timedelta(days=1),  # Invalid: past date
        "status": MaintenanceStatus.SCHEDULED,
        "priority": MaintenancePriority.MEDIUM,
        "description": "Regular maintenance check",
        "technician": "maintenance_tech",
        "estimated_duration": 120,
        "parts_required": ["filter", "lubricant"],
        "notes": "Standard maintenance procedure"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MaintenanceRecordCreate(**test_data)
    assert "Scheduled date cannot be in the past" in str(exc_info.value)

def test_invalid_technician():
    now = datetime.now()
    
    test_data = {
        "record_id": "MNT-004",
        "equipment_id": "EQ-001",
        "maintenance_type": MaintenanceType.PREVENTIVE,
        "scheduled_date": now + timedelta(days=7),
        "status": MaintenanceStatus.SCHEDULED,
        "priority": MaintenancePriority.MEDIUM,
        "description": "Regular maintenance check",
        "technician": "",  # Invalid: empty technician
        "estimated_duration": 120,
        "parts_required": ["filter", "lubricant"],
        "notes": "Standard maintenance procedure"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MaintenanceRecordCreate(**test_data)
    assert "Technician cannot be empty" in str(exc_info.value)

def test_invalid_duration():
    now = datetime.now()
    
    test_data = {
        "record_id": "MNT-005",
        "equipment_id": "EQ-001",
        "maintenance_type": MaintenanceType.PREVENTIVE,
        "scheduled_date": now + timedelta(days=7),
        "status": MaintenanceStatus.SCHEDULED,
        "priority": MaintenancePriority.MEDIUM,
        "description": "Regular maintenance check",
        "technician": "maintenance_tech",
        "estimated_duration": -120,  # Invalid: negative duration
        "parts_required": ["filter", "lubricant"],
        "notes": "Standard maintenance procedure"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MaintenanceRecordCreate(**test_data)
    assert "Duration must be positive" in str(exc_info.value)

def test_completed_maintenance():
    now = datetime.now()
    
    test_data = {
        "record_id": "MNT-006",
        "equipment_id": "EQ-001",
        "maintenance_type": MaintenanceType.CORRECTIVE,
        "scheduled_date": now - timedelta(days=1),
        "status": MaintenanceStatus.COMPLETED,
        "priority": MaintenancePriority.HIGH,
        "description": "Emergency repair",
        "technician": "maintenance_tech",
        "estimated_duration": 240,
        "parts_required": ["motor", "bearings"],
        "notes": "Completed repair",
        "completion_date": now,
        "actual_duration": 180,
        "parts_used": ["motor"],
        "cost": 1500.00
    }
    
    record = MaintenanceRecordCreate(**test_data)
    assert record.status == MaintenanceStatus.COMPLETED
    assert record.completion_date is not None
    assert record.actual_duration == 180
    assert record.parts_used == ["motor"]
    assert record.cost == 1500.00 