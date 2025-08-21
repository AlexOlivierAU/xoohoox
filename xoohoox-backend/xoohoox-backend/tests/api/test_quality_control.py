import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_create_quality_check():
    """Test quality check creation endpoint."""
    test_data = {
        "check_id": "QC-001",
        "batch_id": "BATCH-001",
        "test_date": datetime.now().isoformat(),
        "operator": "quality_operator",
        "test_type": "PH",
        "parameters": {
            "ph": 3.5,
            "brix": 12.5,
            "temperature": 25.0
        },
        "result": "PASS",
        "notes": "Test quality check creation"
    }
    
    response = client.post(f"{settings.API_V1_STR}/quality/checks/", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["check_id"] == test_data["check_id"]
    assert data["batch_id"] == test_data["batch_id"]
    assert data["test_type"] == test_data["test_type"]

def test_get_quality_check():
    """Test quality check retrieval endpoint."""
    # First create a quality check
    test_data = {
        "check_id": "QC-002",
        "batch_id": "BATCH-002",
        "test_date": datetime.now().isoformat(),
        "operator": "quality_operator",
        "test_type": "MICROBIOLOGICAL",
        "parameters": {
            "yeast_count": 100,
            "mold_count": 0,
            "bacteria_count": 0
        },
        "result": "PASS",
        "notes": "Test quality check retrieval"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/quality/checks/", json=test_data)
    assert create_response.status_code == 200
    
    # Then retrieve it
    response = client.get(f"{settings.API_V1_STR}/quality/checks/{test_data['check_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["check_id"] == test_data["check_id"]
    assert data["batch_id"] == test_data["batch_id"]

def test_update_quality_check():
    """Test quality check update endpoint."""
    # First create a quality check
    test_data = {
        "check_id": "QC-003",
        "batch_id": "BATCH-003",
        "test_date": datetime.now().isoformat(),
        "operator": "quality_operator",
        "test_type": "SENSORY",
        "parameters": {
            "appearance": "GOOD",
            "aroma": "GOOD",
            "taste": "GOOD",
            "texture": "GOOD"
        },
        "result": "PASS",
        "notes": "Test quality check update"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/quality/checks/", json=test_data)
    assert create_response.status_code == 200
    
    # Update the quality check
    update_data = {
        "result": "FAIL",
        "notes": "Updated test quality check",
        "corrective_actions": ["Adjust pH", "Re-test after 24 hours"]
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/quality/checks/{test_data['check_id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == update_data["result"]
    assert data["notes"] == update_data["notes"]
    assert data["corrective_actions"] == update_data["corrective_actions"]

def test_delete_quality_check():
    """Test quality check deletion endpoint."""
    # First create a quality check
    test_data = {
        "check_id": "QC-004",
        "batch_id": "BATCH-004",
        "test_date": datetime.now().isoformat(),
        "operator": "quality_operator",
        "test_type": "CHEMICAL",
        "parameters": {
            "alcohol_content": 12.5,
            "acidity": 0.5,
            "sugar_content": 5.0
        },
        "result": "PASS",
        "notes": "Test quality check deletion"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/quality/checks/", json=test_data)
    assert create_response.status_code == 200
    
    # Delete the quality check
    response = client.delete(f"{settings.API_V1_STR}/quality/checks/{test_data['check_id']}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"{settings.API_V1_STR}/quality/checks/{test_data['check_id']}")
    assert get_response.status_code == 404

def test_invalid_quality_check_creation():
    """Test quality check creation with invalid data."""
    test_data = {
        "check_id": "",  # Invalid: empty check ID
        "batch_id": "BATCH-005",
        "test_date": datetime.now().isoformat(),
        "operator": "quality_operator",
        "test_type": "PH",
        "parameters": {
            "ph": -3.5,  # Invalid: negative pH
            "brix": 12.5,
            "temperature": 25.0
        },
        "result": "INVALID_RESULT",  # Invalid: wrong result
        "notes": "Test invalid quality check"
    }
    
    response = client.post(f"{settings.API_V1_STR}/quality/checks/", json=test_data)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0  # Should have validation errors

def test_quality_check_not_found():
    """Test retrieving non-existent quality check."""
    response = client.get(f"{settings.API_V1_STR}/quality/checks/NONEXISTENT-CHECK")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Quality check not found" in data["detail"] 