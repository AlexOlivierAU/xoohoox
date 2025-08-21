import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_create_maintenance(authorized_client: TestClient):
    response = authorized_client.post(
        "/api/v1/equipment-maintenance/",
        json={
            "maintenance_id": "API-TEST-001",
            "equipment_id": "EQUIP-001",
            "equipment_type": EquipmentType.JUICER,
            "equipment_name": "Test Juicer",
            "manufacturer": "Test Manufacturer",
            "model_number": "TEST-123",
            "serial_number": "SN123456",
            "installation_date": datetime.now().isoformat(),
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "technician_id": "TECH-001",
            "cost": 100.00,
            "parts_replaced": "Test parts",
            "work_performed": "Test maintenance",
            "results": "Test results",
            "next_maintenance_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "requires_shutdown": True,
            "shutdown_duration_hours": 2,
            "notes": "Test notes",
            "is_critical": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_id"] == "API-TEST-001"
    assert data["equipment_id"] == "EQUIP-001"
    assert data["maintenance_status"] == MaintenanceStatus.SCHEDULED

def test_read_maintenance(authorized_client: TestClient):
    # First create a maintenance record
    create_response = authorized_client.post(
        "/api/v1/equipment-maintenance/",
        json={
            "maintenance_id": "API-TEST-002",
            "equipment_id": "EQUIP-002",
            "equipment_type": EquipmentType.PASTEURIZER,
            "equipment_name": "Test Pasteurizer",
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        },
    )
    maintenance_id = create_response.json()["maintenance_id"]
    
    # Test get by maintenance_id
    response = authorized_client.get(f"/api/v1/equipment-maintenance/{maintenance_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_id"] == maintenance_id
    assert data["equipment_id"] == "EQUIP-002"

def test_read_maintenances(authorized_client: TestClient):
    # Create multiple maintenance records
    for i in range(3):
        authorized_client.post(
            "/api/v1/equipment-maintenance/",
            json={
                "maintenance_id": f"API-TEST-00{i+3}",
                "equipment_id": f"EQUIP-00{i+3}",
                "equipment_type": EquipmentType.JUICER,
                "equipment_name": f"Test Juicer {i+3}",
                "maintenance_type": MaintenanceType.PREVENTIVE,
                "maintenance_status": MaintenanceStatus.SCHEDULED,
                "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
            },
        )
    
    # Test get all
    response = authorized_client.get("/api/v1/equipment-maintenance/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    
    # Test filtering
    response = authorized_client.get(
        "/api/v1/equipment-maintenance/",
        params={
            "equipment_id": "EQUIP-003",
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["maintenance_id"] == "API-TEST-003"

def test_update_maintenance(authorized_client: TestClient):
    # First create a maintenance record
    create_response = authorized_client.post(
        "/api/v1/equipment-maintenance/",
        json={
            "maintenance_id": "API-TEST-006",
            "equipment_id": "EQUIP-006",
            "equipment_type": EquipmentType.JUICER,
            "equipment_name": "Test Juicer",
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        },
    )
    maintenance_id = create_response.json()["maintenance_id"]
    
    # Test update
    response = authorized_client.put(
        f"/api/v1/equipment-maintenance/{maintenance_id}",
        json={
            "maintenance_status": MaintenanceStatus.IN_PROGRESS,
            "actual_date": datetime.now().isoformat(),
            "cost": 150.00,
            "notes": "Updated test notes",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_status"] == MaintenanceStatus.IN_PROGRESS
    assert data["cost"] == 150.00
    assert data["notes"] == "Updated test notes"

def test_maintenance_lifecycle(authorized_client: TestClient):
    # First create a maintenance record
    create_response = authorized_client.post(
        "/api/v1/equipment-maintenance/",
        json={
            "maintenance_id": "API-TEST-007",
            "equipment_id": "EQUIP-007",
            "equipment_type": EquipmentType.JUICER,
            "equipment_name": "Test Juicer",
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        },
    )
    maintenance_id = create_response.json()["maintenance_id"]
    
    # Test start maintenance
    response = authorized_client.post(f"/api/v1/equipment-maintenance/{maintenance_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_status"] == MaintenanceStatus.IN_PROGRESS
    assert data["actual_date"] is not None
    
    # Test complete maintenance
    response = authorized_client.post(
        f"/api/v1/equipment-maintenance/{maintenance_id}/complete",
        json={
            "results": "Maintenance completed successfully",
            "next_maintenance_date": (datetime.now() + timedelta(days=30)).isoformat(),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_status"] == MaintenanceStatus.COMPLETED
    assert data["results"] == "Maintenance completed successfully"
    assert data["next_maintenance_date"] is not None

def test_maintenance_delay_cancel(authorized_client: TestClient):
    # First create a maintenance record
    create_response = authorized_client.post(
        "/api/v1/equipment-maintenance/",
        json={
            "maintenance_id": "API-TEST-008",
            "equipment_id": "EQUIP-008",
            "equipment_type": EquipmentType.JUICER,
            "equipment_name": "Test Juicer",
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        },
    )
    maintenance_id = create_response.json()["maintenance_id"]
    
    # Test delay maintenance
    response = authorized_client.post(
        f"/api/v1/equipment-maintenance/{maintenance_id}/delay",
        json={
            "new_date": (datetime.now() + timedelta(days=14)).isoformat(),
            "reason": "Parts not available",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_status"] == MaintenanceStatus.DELAYED
    assert "Parts not available" in data["notes"]
    
    # Test cancel maintenance
    response = authorized_client.post(
        f"/api/v1/equipment-maintenance/{maintenance_id}/cancel",
        json={"reason": "Equipment replaced"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_status"] == MaintenanceStatus.CANCELLED
    assert "Equipment replaced" in data["notes"]

def test_delete_maintenance(authorized_client: TestClient):
    # First create a maintenance record
    create_response = authorized_client.post(
        "/api/v1/equipment-maintenance/",
        json={
            "maintenance_id": "API-TEST-009",
            "equipment_id": "EQUIP-009",
            "equipment_type": EquipmentType.JUICER,
            "equipment_name": "Test Juicer",
            "maintenance_type": MaintenanceType.PREVENTIVE,
            "maintenance_status": MaintenanceStatus.SCHEDULED,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        },
    )
    maintenance_id = create_response.json()["maintenance_id"]
    
    # Test delete
    response = authorized_client.delete(f"/api/v1/equipment-maintenance/{maintenance_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["maintenance_id"] == maintenance_id
    
    # Verify deletion
    response = authorized_client.get(f"/api/v1/equipment-maintenance/{maintenance_id}")
    assert response.status_code == 404

def test_create_maintenance_record():
    """Test maintenance record creation endpoint."""
    test_data = {
        "record_id": "MNT-001",
        "equipment_id": "EQ-001",
        "maintenance_type": "PREVENTIVE",
        "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "status": "SCHEDULED",
        "priority": "MEDIUM",
        "description": "Regular maintenance check",
        "technician": "maintenance_tech",
        "estimated_duration": 120,
        "parts_required": ["filter", "lubricant"],
        "notes": "Test maintenance record creation"
    }
    
    response = client.post(f"{settings.API_V1_STR}/maintenance/", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["record_id"] == test_data["record_id"]
    assert data["equipment_id"] == test_data["equipment_id"]
    assert data["maintenance_type"] == test_data["maintenance_type"]

def test_get_maintenance_record():
    """Test maintenance record retrieval endpoint."""
    # First create a maintenance record
    test_data = {
        "record_id": "MNT-002",
        "equipment_id": "EQ-002",
        "maintenance_type": "CORRECTIVE",
        "scheduled_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "status": "SCHEDULED",
        "priority": "HIGH",
        "description": "Emergency repair",
        "technician": "maintenance_tech",
        "estimated_duration": 240,
        "parts_required": ["motor", "bearings"],
        "notes": "Test maintenance record retrieval"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/maintenance/", json=test_data)
    assert create_response.status_code == 200
    
    # Then retrieve it
    response = client.get(f"{settings.API_V1_STR}/maintenance/{test_data['record_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["record_id"] == test_data["record_id"]
    assert data["equipment_id"] == test_data["equipment_id"]

def test_update_maintenance_record():
    """Test maintenance record update endpoint."""
    # First create a maintenance record
    test_data = {
        "record_id": "MNT-003",
        "equipment_id": "EQ-003",
        "maintenance_type": "PREVENTIVE",
        "scheduled_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "status": "SCHEDULED",
        "priority": "LOW",
        "description": "Regular maintenance",
        "technician": "maintenance_tech",
        "estimated_duration": 60,
        "parts_required": ["filter"],
        "notes": "Test maintenance record update"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/maintenance/", json=test_data)
    assert create_response.status_code == 200
    
    # Update the maintenance record
    update_data = {
        "status": "COMPLETED",
        "notes": "Updated test maintenance",
        "completion_date": datetime.now().isoformat(),
        "actual_duration": 45,
        "parts_used": ["filter"],
        "cost": 150.00
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/maintenance/{test_data['record_id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == update_data["status"]
    assert data["notes"] == update_data["notes"]
    assert data["actual_duration"] == update_data["actual_duration"]
    assert data["cost"] == update_data["cost"]

def test_delete_maintenance_record():
    """Test maintenance record deletion endpoint."""
    # First create a maintenance record
    test_data = {
        "record_id": "MNT-004",
        "equipment_id": "EQ-004",
        "maintenance_type": "PREVENTIVE",
        "scheduled_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "status": "SCHEDULED",
        "priority": "MEDIUM",
        "description": "Regular maintenance",
        "technician": "maintenance_tech",
        "estimated_duration": 90,
        "parts_required": ["filter", "lubricant"],
        "notes": "Test maintenance record deletion"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/maintenance/", json=test_data)
    assert create_response.status_code == 200
    
    # Delete the maintenance record
    response = client.delete(f"{settings.API_V1_STR}/maintenance/{test_data['record_id']}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"{settings.API_V1_STR}/maintenance/{test_data['record_id']}")
    assert get_response.status_code == 404

def test_invalid_maintenance_record_creation():
    """Test maintenance record creation with invalid data."""
    test_data = {
        "record_id": "",  # Invalid: empty record ID
        "equipment_id": "EQ-005",
        "maintenance_type": "INVALID_TYPE",  # Invalid: wrong type
        "scheduled_date": (datetime.now() - timedelta(days=1)).isoformat(),  # Invalid: past date
        "status": "INVALID_STATUS",  # Invalid: wrong status
        "priority": "INVALID_PRIORITY",  # Invalid: wrong priority
        "description": "Test invalid maintenance",
        "technician": "",  # Invalid: empty technician
        "estimated_duration": -120,  # Invalid: negative duration
        "parts_required": ["filter"],
        "notes": "Test invalid maintenance record"
    }
    
    response = client.post(f"{settings.API_V1_STR}/maintenance/", json=test_data)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0  # Should have validation errors

def test_maintenance_record_not_found():
    """Test retrieving non-existent maintenance record."""
    response = client.get(f"{settings.API_V1_STR}/maintenance/NONEXISTENT-RECORD")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Maintenance record not found" in data["detail"] 