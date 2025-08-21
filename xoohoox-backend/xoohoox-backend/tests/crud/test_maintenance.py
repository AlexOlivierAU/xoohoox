from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session

from tests.crud.test_crud import TestCRUDBase
from app.crud.maintenance import crud_maintenance
from app.models.maintenance import Maintenance
from app.models.enums import MaintenanceStatus, MaintenanceType
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate

@pytest.fixture
def maintenance_data() -> dict:
    """
    Fixture providing test data for creating a maintenance record.
    """
    return {
        "equipment_id": 1,
        "type": MaintenanceType.PREVENTIVE,
        "status": MaintenanceStatus.SCHEDULED,
        "description": "Regular equipment checkup",
        "scheduled_date": datetime.now() + timedelta(days=7),
        "completion_date": None,
        "technician_notes": None,
        "cost": None
    }

@pytest.fixture
def maintenance_update_data() -> dict:
    """
    Fixture providing test data for updating a maintenance record.
    """
    return {
        "status": MaintenanceStatus.COMPLETED,
        "completion_date": datetime.now(),
        "technician_notes": "All systems checked and functioning properly",
        "cost": 150.00
    }

@pytest.fixture
def test_maintenance(db: Session, maintenance_data: dict) -> Maintenance:
    """
    Fixture that creates a test maintenance record in the database.
    """
    maintenance_in = MaintenanceCreate(**maintenance_data)
    return crud_maintenance.create(db=db, obj_in=maintenance_in)

class TestCRUDMaintenance(TestCRUDBase):
    """Test suite for Maintenance CRUD operations."""
    
    def test_create_maintenance(self, db: Session, maintenance_data: dict) -> None:
        """Test creating a new maintenance record."""
        maintenance_in = MaintenanceCreate(**maintenance_data)
        maintenance = crud_maintenance.create(db=db, obj_in=maintenance_in)
        
        assert maintenance.equipment_id == maintenance_data["equipment_id"]
        assert maintenance.type == maintenance_data["type"]
        assert maintenance.status == maintenance_data["status"]
        assert maintenance.description == maintenance_data["description"]
    
    def test_get_maintenance(self, db: Session, test_maintenance: Maintenance) -> None:
        """Test retrieving a maintenance record by ID."""
        stored_maintenance = crud_maintenance.get(db=db, id=test_maintenance.id)
        assert stored_maintenance
        assert stored_maintenance.id == test_maintenance.id
        assert stored_maintenance.equipment_id == test_maintenance.equipment_id
        assert stored_maintenance.type == test_maintenance.type
    
    def test_update_maintenance(self, db: Session, test_maintenance: Maintenance, maintenance_update_data: dict) -> None:
        """Test updating an existing maintenance record."""
        maintenance_in = MaintenanceUpdate(**maintenance_update_data)
        updated_maintenance = crud_maintenance.update(
            db=db, 
            db_obj=test_maintenance, 
            obj_in=maintenance_in
        )
        
        assert updated_maintenance.status == maintenance_update_data["status"]
        assert updated_maintenance.completion_date is not None
        assert updated_maintenance.technician_notes == maintenance_update_data["technician_notes"]
        assert updated_maintenance.cost == maintenance_update_data["cost"]
    
    def test_delete_maintenance(self, db: Session, test_maintenance: Maintenance) -> None:
        """Test deleting a maintenance record."""
        maintenance_id = test_maintenance.id
        crud_maintenance.remove(db=db, id=maintenance_id)
        deleted_maintenance = crud_maintenance.get(db=db, id=maintenance_id)
        assert deleted_maintenance is None
    
    def test_maintenance_status_transition(self, db: Session, test_maintenance: Maintenance) -> None:
        """Test transitioning maintenance status from SCHEDULED to IN_PROGRESS to COMPLETED."""
        # Update to IN_PROGRESS
        in_progress_update = MaintenanceUpdate(status=MaintenanceStatus.IN_PROGRESS)
        maintenance = crud_maintenance.update(db=db, db_obj=test_maintenance, obj_in=in_progress_update)
        assert maintenance.status == MaintenanceStatus.IN_PROGRESS
        
        # Update to COMPLETED
        completed_update = MaintenanceUpdate(
            status=MaintenanceStatus.COMPLETED,
            completion_date=datetime.now(),
            technician_notes="Maintenance completed successfully"
        )
        maintenance = crud_maintenance.update(db=db, db_obj=maintenance, obj_in=completed_update)
        assert maintenance.status == MaintenanceStatus.COMPLETED
        assert maintenance.completion_date is not None 