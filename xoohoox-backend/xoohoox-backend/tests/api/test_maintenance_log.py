from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import LogType
from tests.api.test_equipment_maintenance import create_random_equipment_maintenance

def test_create_maintenance_log(
    client: TestClient,
    db_session: Session,
    normal_user_token_headers: dict,
) -> None:
    """Test creating a maintenance log through the API."""
    # First create a maintenance record to reference
    maintenance = create_random_equipment_maintenance(db_session)
    
    data = {
        "maintenance_id": maintenance.id,
        "log_date": datetime.utcnow().isoformat(),
        "log_type": LogType.INSPECTION,
        "description": "Regular equipment inspection",
        "performed_by": "John Doe",
        "notes": "All systems operating normally"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/maintenance-logs/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["maintenance_id"] == data["maintenance_id"]
    assert content["log_type"] == data["log_type"]
    assert content["description"] == data["description"]
    assert content["performed_by"] == data["performed_by"]
    assert content["notes"] == data["notes"]
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content

def test_read_maintenance_logs(
    client: TestClient,
    db_session: Session,
    normal_user_token_headers: dict,
) -> None:
    """Test reading maintenance logs through the API."""
    # First create a maintenance record and some logs
    maintenance = create_random_equipment_maintenance(db_session)
    
    # Create multiple logs
    for i in range(3):
        data = {
            "maintenance_id": maintenance.id,
            "log_date": datetime.utcnow().isoformat(),
            "log_type": LogType.INSPECTION,
            "description": f"Test inspection {i}",
            "performed_by": "John Doe",
            "notes": f"Test notes {i}"
        }
        response = client.post(
            f"{settings.API_V1_STR}/maintenance-logs/",
            headers=normal_user_token_headers,
            json=data,
        )
        assert response.status_code == 200
    
    # Test reading all logs
    response = client.get(
        f"{settings.API_V1_STR}/maintenance-logs/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 3
    
    # Test reading logs by maintenance_id
    response = client.get(
        f"{settings.API_V1_STR}/maintenance-logs/?maintenance_id={maintenance.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 3
    assert all(log["maintenance_id"] == maintenance.id for log in content)
    
    # Test reading logs by performed_by
    response = client.get(
        f"{settings.API_V1_STR}/maintenance-logs/?performed_by=John Doe",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 3
    assert all(log["performed_by"] == "John Doe" for log in content)

def test_read_maintenance_log(
    client: TestClient,
    db_session: Session,
    normal_user_token_headers: dict,
) -> None:
    """Test reading a specific maintenance log through the API."""
    # First create a maintenance record and a log
    maintenance = create_random_equipment_maintenance(db_session)
    
    data = {
        "maintenance_id": maintenance.id,
        "log_date": datetime.utcnow().isoformat(),
        "log_type": LogType.INSPECTION,
        "description": "Test inspection",
        "performed_by": "John Doe",
        "notes": "Test notes"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/maintenance-logs/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    log_id = content["id"]
    
    # Test reading the specific log
    response = client.get(
        f"{settings.API_V1_STR}/maintenance-logs/{log_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == log_id
    assert content["maintenance_id"] == maintenance.id
    assert content["log_type"] == data["log_type"]
    assert content["description"] == data["description"]
    assert content["performed_by"] == data["performed_by"]
    assert content["notes"] == data["notes"]

def test_update_maintenance_log(
    client: TestClient,
    db_session: Session,
    normal_user_token_headers: dict,
) -> None:
    """Test updating a maintenance log through the API."""
    # First create a maintenance record and a log
    maintenance = create_random_equipment_maintenance(db_session)
    
    data = {
        "maintenance_id": maintenance.id,
        "log_date": datetime.utcnow().isoformat(),
        "log_type": LogType.INSPECTION,
        "description": "Test inspection",
        "performed_by": "John Doe",
        "notes": "Test notes"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/maintenance-logs/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    log_id = content["id"]
    
    # Test updating the log
    update_data = {
        "description": "Updated inspection notes",
        "notes": "Updated test notes"
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/maintenance-logs/{log_id}",
        headers=normal_user_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == log_id
    assert content["description"] == update_data["description"]
    assert content["notes"] == update_data["notes"]
    assert content["maintenance_id"] == maintenance.id
    assert content["log_type"] == data["log_type"]
    assert content["performed_by"] == data["performed_by"]

def test_delete_maintenance_log(
    client: TestClient,
    db_session: Session,
    normal_user_token_headers: dict,
) -> None:
    """Test deleting a maintenance log through the API."""
    # First create a maintenance record and a log
    maintenance = create_random_equipment_maintenance(db_session)
    
    data = {
        "maintenance_id": maintenance.id,
        "log_date": datetime.utcnow().isoformat(),
        "log_type": LogType.INSPECTION,
        "description": "Test inspection",
        "performed_by": "John Doe",
        "notes": "Test notes"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/maintenance-logs/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    log_id = content["id"]
    
    # Test deleting the log
    response = client.delete(
        f"{settings.API_V1_STR}/maintenance-logs/{log_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == log_id
    
    # Verify the log is no longer accessible
    response = client.get(
        f"{settings.API_V1_STR}/maintenance-logs/{log_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 404 