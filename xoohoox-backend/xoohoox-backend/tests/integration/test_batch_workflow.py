import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_complete_batch_workflow():
    """Test the complete workflow from batch creation to quality check to maintenance."""
    
    # 1. Login as superuser
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    
    login_response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create a new batch
    batch_data = {
        "batch_id": "TEST-WORKFLOW-001",
        "product_type": "Orange Juice",
        "quantity": 1000,
        "start_date": datetime.now().isoformat(),
        "expected_completion_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "status": "In Progress",
        "notes": "Test complete workflow"
    }
    
    batch_response = client.post(
        f"{settings.API_V1_STR}/batches/",
        headers=headers,
        json=batch_data
    )
    assert batch_response.status_code == 200
    batch_id = batch_response.json()["batch_id"]
    
    # 3. Create a quality check for the batch
    quality_data = {
        "check_id": "QC-WORKFLOW-001",
        "batch_id": batch_id,
        "test_date": datetime.now().isoformat(),
        "operator": "quality_operator",
        "test_type": "PH",
        "parameters": {
            "ph": 3.5,
            "brix": 12.5,
            "temperature": 25.0
        },
        "result": "PASS",
        "notes": "Test workflow quality check"
    }
    
    quality_response = client.post(
        f"{settings.API_V1_STR}/quality/checks/",
        headers=headers,
        json=quality_data
    )
    assert quality_response.status_code == 200
    check_id = quality_response.json()["check_id"]
    
    # 4. Create a maintenance record for equipment used
    maintenance_data = {
        "record_id": "MNT-WORKFLOW-001",
        "equipment_id": "EQ-001",
        "maintenance_type": "PREVENTIVE",
        "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "status": "SCHEDULED",
        "priority": "MEDIUM",
        "description": "Regular maintenance after batch processing",
        "technician": "maintenance_tech",
        "estimated_duration": 120,
        "parts_required": ["filter", "lubricant"],
        "notes": "Test workflow maintenance"
    }
    
    maintenance_response = client.post(
        f"{settings.API_V1_STR}/maintenance/",
        headers=headers,
        json=maintenance_data
    )
    assert maintenance_response.status_code == 200
    maintenance_id = maintenance_response.json()["record_id"]
    
    # 5. Update batch status to completed
    batch_update = {
        "status": "Completed",
        "notes": "Batch processing completed successfully"
    }
    
    batch_update_response = client.put(
        f"{settings.API_V1_STR}/batches/{batch_id}",
        headers=headers,
        json=batch_update
    )
    assert batch_update_response.status_code == 200
    assert batch_update_response.json()["status"] == "Completed"
    
    # 6. Complete the maintenance record
    maintenance_update = {
        "status": "COMPLETED",
        "notes": "Maintenance completed successfully",
        "completion_date": datetime.now().isoformat(),
        "actual_duration": 90,
        "parts_used": ["filter"],
        "cost": 150.00
    }
    
    maintenance_update_response = client.put(
        f"{settings.API_V1_STR}/maintenance/{maintenance_id}",
        headers=headers,
        json=maintenance_update
    )
    assert maintenance_update_response.status_code == 200
    assert maintenance_update_response.json()["status"] == "COMPLETED"
    
    # 7. Verify all records are properly linked
    # Get batch details
    batch_details = client.get(
        f"{settings.API_V1_STR}/batches/{batch_id}",
        headers=headers
    )
    assert batch_details.status_code == 200
    assert batch_details.json()["status"] == "Completed"
    
    # Get quality check details
    quality_details = client.get(
        f"{settings.API_V1_STR}/quality/checks/{check_id}",
        headers=headers
    )
    assert quality_details.status_code == 200
    assert quality_details.json()["batch_id"] == batch_id
    
    # Get maintenance details
    maintenance_details = client.get(
        f"{settings.API_V1_STR}/maintenance/{maintenance_id}",
        headers=headers
    )
    assert maintenance_details.status_code == 200
    assert maintenance_details.json()["status"] == "COMPLETED" 