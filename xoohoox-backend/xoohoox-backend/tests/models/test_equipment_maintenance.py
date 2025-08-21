import pytest
from datetime import datetime, timedelta
from app.models.equipment_maintenance import EquipmentMaintenance
from app.models.enums import MaintenanceType, MaintenancePriority, EquipmentStatus

def test_equipment_maintenance_creation():
    """Test creating an equipment maintenance record with valid data."""
    actual_date = datetime.utcnow()
    next_date = actual_date + timedelta(days=90)
    
    maintenance = EquipmentMaintenance(
        equipment_id=1,
        maintenance_type=MaintenanceType.PREVENTIVE,
        priority=MaintenancePriority.HIGH,
        description="Regular maintenance check",
        actual_date=actual_date,
        next_maintenance_date=next_date,
        performed_by=1,
        cost=150.50,
        parts_used="Filter, Oil",
        notes="Completed as scheduled"
    )
    
    assert maintenance.equipment_id == 1
    assert maintenance.maintenance_type == MaintenanceType.PREVENTIVE
    assert maintenance.priority == MaintenancePriority.HIGH
    assert maintenance.description == "Regular maintenance check"
    assert maintenance.actual_date == actual_date
    assert maintenance.next_maintenance_date == next_date
    assert maintenance.performed_by == 1
    assert maintenance.cost == 150.50
    assert maintenance.parts_used == "Filter, Oil"
    assert maintenance.notes == "Completed as scheduled"

def test_equipment_maintenance_defaults():
    """Test default values for equipment maintenance fields."""
    maintenance = EquipmentMaintenance(
        equipment_id=1,
        maintenance_type=MaintenanceType.PREVENTIVE,
        description="Regular maintenance check",
        performed_by=1
    )
    
    assert maintenance.priority == MaintenancePriority.MEDIUM  # Should default to MEDIUM
    assert maintenance.cost == 0.0  # Should default to 0
    assert maintenance.parts_used is None
    assert maintenance.notes is None
    assert isinstance(maintenance.actual_date, datetime)  # Should default to current time

def test_equipment_maintenance_representation():
    """Test string representation of EquipmentMaintenance model."""
    maintenance = EquipmentMaintenance(
        equipment_id=1,
        maintenance_type=MaintenanceType.PREVENTIVE,
        description="Regular maintenance check",
        performed_by=1
    )
    
    str_repr = str(maintenance)
    assert "EquipmentMaintenance" in str_repr
    assert "PREVENTIVE" in str_repr
    assert "Regular maintenance check" in str_repr

def test_equipment_maintenance_to_dict():
    """Test the to_dict method of EquipmentMaintenance model."""
    actual_date = datetime.utcnow()
    next_date = actual_date + timedelta(days=90)
    
    maintenance = EquipmentMaintenance(
        equipment_id=1,
        maintenance_type=MaintenanceType.PREVENTIVE,
        priority=MaintenancePriority.HIGH,
        description="Regular maintenance check",
        actual_date=actual_date,
        next_maintenance_date=next_date,
        performed_by=1,
        cost=150.50,
        parts_used="Filter, Oil",
        notes="Completed as scheduled"
    )
    
    maint_dict = maintenance.to_dict()
    
    assert maint_dict['equipment_id'] == 1
    assert maint_dict['maintenance_type'] == MaintenanceType.PREVENTIVE.value
    assert maint_dict['priority'] == MaintenancePriority.HIGH.value
    assert maint_dict['description'] == "Regular maintenance check"
    assert 'actual_date' in maint_dict
    assert 'next_maintenance_date' in maint_dict
    assert maint_dict['performed_by'] == 1
    assert maint_dict['cost'] == 150.50
    assert maint_dict['parts_used'] == "Filter, Oil"
    assert maint_dict['notes'] == "Completed as scheduled"

def test_equipment_maintenance_validation():
    """Test equipment maintenance validation rules."""
    actual_date = datetime.utcnow()
    
    # Test invalid cost (negative)
    with pytest.raises(ValueError):
        EquipmentMaintenance(
            equipment_id=1,
            maintenance_type=MaintenanceType.PREVENTIVE,
            description="Regular maintenance check",
            performed_by=1,
            cost=-50.0  # Negative cost
        )
    
    # Test invalid next maintenance date (before actual date)
    with pytest.raises(ValueError):
        EquipmentMaintenance(
            equipment_id=1,
            maintenance_type=MaintenanceType.PREVENTIVE,
            description="Regular maintenance check",
            performed_by=1,
            actual_date=actual_date,
            next_maintenance_date=actual_date - timedelta(days=1)  # Earlier than actual date
        )

def test_equipment_maintenance_status_update():
    """Test equipment status updates based on maintenance."""
    maintenance = EquipmentMaintenance(
        equipment_id=1,
        maintenance_type=MaintenanceType.PREVENTIVE,
        description="Regular maintenance check",
        performed_by=1
    )
    
    # Test status during maintenance
    maintenance.start_maintenance()
    assert maintenance.equipment_status == EquipmentStatus.MAINTENANCE
    
    # Test status after completion
    maintenance.complete_maintenance()
    assert maintenance.equipment_status == EquipmentStatus.OPERATIONAL
    
    # Test emergency maintenance
    emergency = EquipmentMaintenance(
        equipment_id=1,
        maintenance_type=MaintenanceType.EMERGENCY,
        description="Emergency repair",
        performed_by=1
    )
    assert emergency.priority == MaintenancePriority.CRITICAL  # Should auto-set to CRITICAL for emergency 