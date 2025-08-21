import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_create_batch():
    """Test batch creation endpoint."""
    test_data = {
        "batch_id": "TEST-BATCH-001",
        "product_type": "Orange Juice",
        "quantity": 1000,
        "start_date": datetime.now().isoformat(),
        "expected_completion_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "status": "In Progress",
        "notes": "Test batch creation"
    }
    
    response = client.post(f"{settings.API_V1_STR}/batches/", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == test_data["batch_id"]
    assert data["product_type"] == test_data["product_type"]
    assert data["quantity"] == test_data["quantity"]

def test_get_batch():
    """Test batch retrieval endpoint."""
    # First create a batch
    test_data = {
        "batch_id": "TEST-BATCH-002",
        "product_type": "Apple Juice",
        "quantity": 500,
        "start_date": datetime.now().isoformat(),
        "expected_completion_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "status": "In Progress",
        "notes": "Test batch retrieval"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/batches/", json=test_data)
    assert create_response.status_code == 200
    
    # Then retrieve it
    response = client.get(f"{settings.API_V1_STR}/batches/{test_data['batch_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == test_data["batch_id"]
    assert data["product_type"] == test_data["product_type"]

def test_update_batch():
    """Test batch update endpoint."""
    # First create a batch
    test_data = {
        "batch_id": "TEST-BATCH-003",
        "product_type": "Grape Juice",
        "quantity": 750,
        "start_date": datetime.now().isoformat(),
        "expected_completion_date": (datetime.now() + timedelta(days=6)).isoformat(),
        "status": "In Progress",
        "notes": "Test batch update"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/batches/", json=test_data)
    assert create_response.status_code == 200
    
    # Update the batch
    update_data = {
        "quantity": 800,
        "status": "Completed",
        "notes": "Updated test batch"
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/batches/{test_data['batch_id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == update_data["quantity"]
    assert data["status"] == update_data["status"]
    assert data["notes"] == update_data["notes"]

def test_delete_batch():
    """Test batch deletion endpoint."""
    # First create a batch
    test_data = {
        "batch_id": "TEST-BATCH-004",
        "product_type": "Pineapple Juice",
        "quantity": 600,
        "start_date": datetime.now().isoformat(),
        "expected_completion_date": (datetime.now() + timedelta(days=4)).isoformat(),
        "status": "In Progress",
        "notes": "Test batch deletion"
    }
    
    create_response = client.post(f"{settings.API_V1_STR}/batches/", json=test_data)
    assert create_response.status_code == 200
    
    # Delete the batch
    response = client.delete(f"{settings.API_V1_STR}/batches/{test_data['batch_id']}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"{settings.API_V1_STR}/batches/{test_data['batch_id']}")
    assert get_response.status_code == 404

def test_invalid_batch_creation():
    """Test batch creation with invalid data."""
    test_data = {
        "batch_id": "",  # Invalid: empty batch ID
        "product_type": "Orange Juice",
        "quantity": -100,  # Invalid: negative quantity
        "start_date": datetime.now().isoformat(),
        "expected_completion_date": (datetime.now() - timedelta(days=1)).isoformat(),  # Invalid: past date
        "status": "Invalid Status",  # Invalid: wrong status
        "notes": "Test invalid batch"
    }
    
    response = client.post(f"{settings.API_V1_STR}/batches/", json=test_data)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0  # Should have validation errors

def test_batch_not_found():
    """Test retrieving non-existent batch."""
    response = client.get(f"{settings.API_V1_STR}/batches/NONEXISTENT-BATCH")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Batch not found" in data["detail"] 