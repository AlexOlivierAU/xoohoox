import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.crud.equipment_maintenance import (
    equipment_maintenance,
    get_by_maintenance_id,
    start_maintenance,
    complete_maintenance,
    delay_maintenance,
    cancel_maintenance,
)
from app.models.equipment_maintenance import (
    EquipmentMaintenance,
    MaintenanceType,
    MaintenanceStatus,
    EquipmentType,
)
from app.schemas.equipment_maintenance import (
    EquipmentMaintenanceCreate,
    EquipmentMaintenanceUpdate,
)

def test_create_maintenance(db: Session):
    maintenance_in = EquipmentMaintenanceCreate(
        maintenance_id="TEST-MAINT-001",
        equipment_id="EQUIP-001",
        equipment_type=EquipmentType.JUICER,
        equipment_name="Test Juicer",
        manufacturer="Test Manufacturer",
        model_number="TEST-123",
        serial_number="SN123456",
        installation_date=datetime.now(),
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
        scheduled_date=datetime.now() + timedelta(days=7),
        technician_id="TECH-001",
        cost=100.00,
        parts_replaced="Test parts",
        work_performed="Test maintenance",
        results="Test results",
        next_maintenance_date=datetime.now() + timedelta(days=30),
        requires_shutdown=True,
        shutdown_duration_hours=2,
        notes="Test notes",
        is_critical=False,
    )
    
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    assert maintenance.maintenance_id == maintenance_in.maintenance_id
    assert maintenance.equipment_id == maintenance_in.equipment_id
    assert maintenance.maintenance_status == MaintenanceStatus.SCHEDULED

def test_get_maintenance(db: Session):
    # Create test maintenance
    maintenance_in = EquipmentMaintenanceCreate(
        maintenance_id="TEST-MAINT-002",
        equipment_id="EQUIP-002",
        equipment_type=EquipmentType.PASTEURIZER,
        equipment_name="Test Pasteurizer",
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
        scheduled_date=datetime.now() + timedelta(days=7),
    )
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    
    # Test get by ID
    retrieved = equipment_maintenance.get(db, id=maintenance.id)
    assert retrieved is not None
    assert retrieved.maintenance_id == maintenance_in.maintenance_id
    
    # Test get by maintenance_id
    retrieved = get_by_maintenance_id(db, maintenance_id=maintenance_in.maintenance_id)
    assert retrieved is not None
    assert retrieved.equipment_id == maintenance_in.equipment_id

def test_get_multi_maintenance(db: Session):
    # Create multiple test maintenances
    maintenances = []
    for i in range(3):
        maintenance_in = EquipmentMaintenanceCreate(
            maintenance_id=f"TEST-MAINT-00{i+3}",
            equipment_id=f"EQUIP-00{i+3}",
            equipment_type=EquipmentType.JUICER,
            equipment_name=f"Test Juicer {i+3}",
            maintenance_type=MaintenanceType.PREVENTIVE,
            maintenance_status=MaintenanceStatus.SCHEDULED,
            scheduled_date=datetime.now() + timedelta(days=7),
        )
        maintenances.append(equipment_maintenance.create(db, obj_in=maintenance_in))
    
    # Test get_multi
    retrieved = equipment_maintenance.get_multi(db)
    assert len(retrieved) >= 3
    
    # Test filtering
    filtered = equipment_maintenance.get_multi(
        db,
        equipment_id="EQUIP-003",
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
    )
    assert len(filtered) == 1
    assert filtered[0].maintenance_id == "TEST-MAINT-003"

def test_update_maintenance(db: Session):
    # Create test maintenance
    maintenance_in = EquipmentMaintenanceCreate(
        maintenance_id="TEST-MAINT-006",
        equipment_id="EQUIP-006",
        equipment_type=EquipmentType.JUICER,
        equipment_name="Test Juicer",
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
        scheduled_date=datetime.now() + timedelta(days=7),
    )
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    
    # Test update
    update_data = EquipmentMaintenanceUpdate(
        maintenance_status=MaintenanceStatus.IN_PROGRESS,
        actual_date=datetime.now(),
        cost=150.00,
        notes="Updated test notes",
    )
    updated = equipment_maintenance.update(db, db_obj=maintenance, obj_in=update_data)
    assert updated.maintenance_status == MaintenanceStatus.IN_PROGRESS
    assert updated.cost == 150.00
    assert updated.notes == "Updated test notes"

def test_maintenance_lifecycle(db: Session):
    # Create test maintenance
    maintenance_in = EquipmentMaintenanceCreate(
        maintenance_id="TEST-MAINT-007",
        equipment_id="EQUIP-007",
        equipment_type=EquipmentType.JUICER,
        equipment_name="Test Juicer",
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
        scheduled_date=datetime.now() + timedelta(days=7),
    )
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    
    # Test start maintenance
    started = start_maintenance(db, maintenance_id=maintenance.maintenance_id)
    assert started.maintenance_status == MaintenanceStatus.IN_PROGRESS
    assert started.actual_date is not None
    
    # Test complete maintenance
    completed = complete_maintenance(
        db,
        maintenance_id=maintenance.maintenance_id,
        results="Maintenance completed successfully",
        next_maintenance_date=datetime.now() + timedelta(days=30),
    )
    assert completed.maintenance_status == MaintenanceStatus.COMPLETED
    assert completed.results == "Maintenance completed successfully"
    assert completed.next_maintenance_date is not None

def test_maintenance_delay_cancel(db: Session):
    # Create test maintenance
    maintenance_in = EquipmentMaintenanceCreate(
        maintenance_id="TEST-MAINT-008",
        equipment_id="EQUIP-008",
        equipment_type=EquipmentType.JUICER,
        equipment_name="Test Juicer",
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
        scheduled_date=datetime.now() + timedelta(days=7),
    )
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    
    # Test delay maintenance
    delayed = delay_maintenance(
        db,
        maintenance_id=maintenance.maintenance_id,
        new_date=datetime.now() + timedelta(days=14),
        reason="Parts not available",
    )
    assert delayed.maintenance_status == MaintenanceStatus.DELAYED
    assert delayed.scheduled_date == datetime.now() + timedelta(days=14)
    assert "Parts not available" in delayed.notes
    
    # Test cancel maintenance
    cancelled = cancel_maintenance(
        db,
        maintenance_id=maintenance.maintenance_id,
        reason="Equipment replaced",
    )
    assert cancelled.maintenance_status == MaintenanceStatus.CANCELLED
    assert "Equipment replaced" in cancelled.notes

def test_remove_maintenance(db: Session):
    # Create test maintenance
    maintenance_in = EquipmentMaintenanceCreate(
        maintenance_id="TEST-MAINT-009",
        equipment_id="EQUIP-009",
        equipment_type=EquipmentType.JUICER,
        equipment_name="Test Juicer",
        maintenance_type=MaintenanceType.PREVENTIVE,
        maintenance_status=MaintenanceStatus.SCHEDULED,
        scheduled_date=datetime.now() + timedelta(days=7),
    )
    maintenance = equipment_maintenance.create(db, obj_in=maintenance_in)
    
    # Test remove
    removed = equipment_maintenance.remove(db, id=maintenance.id)
    assert removed is not None
    
    # Verify removal
    retrieved = equipment_maintenance.get(db, id=maintenance.id)
    assert retrieved is None 