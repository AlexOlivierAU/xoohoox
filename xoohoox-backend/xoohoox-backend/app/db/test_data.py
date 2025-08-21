from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.crud import batch_tracking
from app.schemas.batch_tracking import BatchTrackingCreate

def create_test_batches(db: Session) -> None:
    """Create test batch data if none exists."""
    
    # Test batch data
    test_batches = [
        {
            "batch_id": "B001",
            "name": "Apple Juice Batch 1",
            "status": "in_progress",
            "stage": "fermentation",
            "progress": 75.0,
            "start_date": datetime.now() - timedelta(days=5),
            "end_date": datetime.now() + timedelta(days=5)
        },
        {
            "batch_id": "B002",
            "name": "Pear Juice Batch 1",
            "status": "planned",
            "stage": "initial",
            "progress": 0.0,
            "start_date": datetime.now() + timedelta(days=1),
            "end_date": datetime.now() + timedelta(days=10)
        }
    ]
    
    for batch_data in test_batches:
        # Check if batch already exists
        existing_batch = batch_tracking.get_by_batch_id(db, batch_id=batch_data["batch_id"])
        if not existing_batch:
            batch_in = BatchTrackingCreate(**batch_data)
            batch_tracking.create(db, obj_in=batch_in) 