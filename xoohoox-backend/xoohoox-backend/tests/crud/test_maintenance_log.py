from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session

from app.crud.maintenance_log import maintenance_log
from app.models.maintenance_log import MaintenanceLog
from app.models.enums import LogType
from app.schemas.maintenance_log import MaintenanceLogCreate, MaintenanceLogUpdate

@pytest.fixture
def maintenance_log_data() -> dict:
    """Fixture for basic maintenance log data."""
    return {
        "maintenance_id": 1,
        "log_date": datetime.utcnow(),
        "log_type": LogType.INSPECTION,
        "description": "Regular equipment inspection",
        "performed_by": "John Doe",
        "notes": "All systems operating normally"
    }

@pytest.fixture
def test_maintenance_log(db_session: Session, maintenance_log_data) -> MaintenanceLog:
    """Fixture that creates a test maintenance log record in the database."""
    log = MaintenanceLog(**maintenance_log_data)
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)
    return log

def test_create_maintenance_log(db_session: Session, maintenance_log_data):
    """Test creating a maintenance log with valid data."""
    log = maintenance_log.create(db=db_session, obj_in=MaintenanceLogCreate(**maintenance_log_data))
    
    assert log.id is not None
    assert log.maintenance_id == maintenance_log_data["maintenance_id"]
    assert log.log_date == maintenance_log_data["log_date"]
    assert log.log_type == maintenance_log_data["log_type"]
    assert log.description == maintenance_log_data["description"]
    assert log.performed_by == maintenance_log_data["performed_by"]
    assert log.notes == maintenance_log_data["notes"]

def test_read_maintenance_log(db_session: Session, test_maintenance_log):
    """Test reading a maintenance log from the database."""
    stored_log = maintenance_log.get(db=db_session, id=test_maintenance_log.id)
    assert stored_log is not None
    assert stored_log.maintenance_id == test_maintenance_log.maintenance_id
    assert stored_log.log_type == test_maintenance_log.log_type
    assert stored_log.description == test_maintenance_log.description
    assert stored_log.performed_by == test_maintenance_log.performed_by

def test_update_maintenance_log(db_session: Session, test_maintenance_log):
    """Test updating a maintenance log."""
    update_data = {
        "description": "Updated inspection notes",
        "notes": "Minor adjustments needed"
    }
    updated_log = maintenance_log.update(
        db=db_session,
        db_obj=test_maintenance_log,
        obj_in=MaintenanceLogUpdate(**update_data)
    )
    
    assert updated_log.description == update_data["description"]
    assert updated_log.notes == update_data["notes"]
    assert updated_log.maintenance_id == test_maintenance_log.maintenance_id
    assert updated_log.log_type == test_maintenance_log.log_type

def test_delete_maintenance_log(db_session: Session, test_maintenance_log):
    """Test deleting a maintenance log."""
    deleted_log = maintenance_log.remove(db=db_session, id=test_maintenance_log.id)
    assert deleted_log.id == test_maintenance_log.id
    
    # Verify the log is no longer in the database
    stored_log = maintenance_log.get(db=db_session, id=test_maintenance_log.id)
    assert stored_log is None

def test_get_by_maintenance_id(db_session: Session, test_maintenance_log):
    """Test retrieving maintenance logs by maintenance ID."""
    logs = maintenance_log.get_by_maintenance_id(
        db=db_session,
        maintenance_id=test_maintenance_log.maintenance_id
    )
    assert len(logs) > 0
    assert all(log.maintenance_id == test_maintenance_log.maintenance_id for log in logs)

def test_get_by_performed_by(db_session: Session, test_maintenance_log):
    """Test retrieving maintenance logs by performer."""
    logs = maintenance_log.get_by_performed_by(
        db=db_session,
        performed_by=test_maintenance_log.performed_by
    )
    assert len(logs) > 0
    assert all(log.performed_by == test_maintenance_log.performed_by for log in logs) 