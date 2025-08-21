import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.enums import EquipmentType, EquipmentStatus

@pytest.fixture
def equipment_data():
    """Fixture for basic equipment data."""
    return {
        "name": "Test Juicer",
        "type": EquipmentType.JUICER,
        "status": EquipmentStatus.OPERATIONAL,
        "capacity": 1000.0,
        "description": "Industrial juice extractor",
        "manufacturer": "JuiceTech",
        "model_number": "JT-2000",
        "serial_number": "JT2000-123",
        "installation_date": datetime.utcnow(),
        "is_critical": True,
        "location": "Production Line A"
    }

@pytest.fixture
def test_equipment(db_session: Session, equipment_data):
    """Fixture that creates a test equipment record in the database."""
    equipment = Equipment(**equipment_data)
    db_session.add(equipment)
    db_session.commit()
    db_session.refresh(equipment)
    return equipment

def test_create_equipment(db_session: Session, equipment_data):
    """Test creating equipment with valid data."""
    equipment = Equipment(**equipment_data)
    db_session.add(equipment)
    db_session.commit()
    db_session.refresh(equipment)
    
    assert equipment.id is not None
    assert equipment.name == equipment_data["name"]
    assert equipment.type == equipment_data["type"]
    assert equipment.status == equipment_data["status"]
    assert equipment.capacity == equipment_data["capacity"]
    assert equipment.description == equipment_data["description"]
    assert equipment.manufacturer == equipment_data["manufacturer"]
    assert equipment.model_number == equipment_data["model_number"]
    assert equipment.serial_number == equipment_data["serial_number"]
    assert isinstance(equipment.installation_date, datetime)
    assert equipment.is_critical == equipment_data["is_critical"]
    assert equipment.location == equipment_data["location"]

def test_read_equipment(db_session: Session, test_equipment):
    """Test reading equipment from the database."""
    stored_equipment = db_session.query(Equipment).filter(Equipment.id == test_equipment.id).first()
    assert stored_equipment is not None
    assert stored_equipment.name == test_equipment.name
    assert stored_equipment.type == test_equipment.type
    assert stored_equipment.status == test_equipment.status

def test_update_equipment(db_session: Session, test_equipment):
    """Test updating equipment attributes."""
    test_equipment.name = "Updated Juicer"
    test_equipment.status = EquipmentStatus.MAINTENANCE
    test_equipment.capacity = 1500.0
    db_session.commit()
    db_session.refresh(test_equipment)
    
    updated_equipment = db_session.query(Equipment).filter(Equipment.id == test_equipment.id).first()
    assert updated_equipment.name == "Updated Juicer"
    assert updated_equipment.status == EquipmentStatus.MAINTENANCE
    assert updated_equipment.capacity == 1500.0

def test_delete_equipment(db_session: Session, test_equipment):
    """Test deleting equipment from the database."""
    db_session.delete(test_equipment)
    db_session.commit()
    
    deleted_equipment = db_session.query(Equipment).filter(Equipment.id == test_equipment.id).first()
    assert deleted_equipment is None

def test_equipment_status_transition(db_session: Session, test_equipment):
    """Test equipment status transitions."""
    # Test transition to MAINTENANCE
    test_equipment.status = EquipmentStatus.MAINTENANCE
    db_session.commit()
    assert test_equipment.status == EquipmentStatus.MAINTENANCE
    
    # Test transition to REPAIR
    test_equipment.status = EquipmentStatus.REPAIR
    db_session.commit()
    assert test_equipment.status == EquipmentStatus.REPAIR
    
    # Test transition back to OPERATIONAL
    test_equipment.status = EquipmentStatus.OPERATIONAL
    db_session.commit()
    assert test_equipment.status == EquipmentStatus.OPERATIONAL

def test_equipment_defaults(db_session: Session):
    """Test default values for equipment fields."""
    equipment = Equipment(
        name="Basic Equipment",
        type=EquipmentType.OTHER
    )
    db_session.add(equipment)
    db_session.commit()
    db_session.refresh(equipment)
    
    assert equipment.status == EquipmentStatus.OPERATIONAL
    assert equipment.capacity is None
    assert equipment.description is None
    assert equipment.manufacturer is None
    assert equipment.model_number is None
    assert equipment.serial_number is None
    assert equipment.installation_date is None
    assert equipment.last_maintenance_date is None
    assert equipment.next_maintenance_date is None
    assert equipment.is_critical is False
    assert equipment.location is None
    assert equipment.notes is None 