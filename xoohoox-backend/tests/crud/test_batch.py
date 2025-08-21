from datetime import datetime, timedelta
from app.models.batch import Batch
from app.models.enums import BatchStatus, FruitType, JuiceType
from tests.crud.test_crud import TestCRUDBase

class TestBatchCRUD(TestCRUDBase):
    model_class = Batch
    create_data = {
        "name": "Test Batch",
        "fruit_type": FruitType.APPLE,
        "juice_type": JuiceType.FRESH,
        "target_volume": 100.0,
        "notes": "Test batch for CRUD operations",
        "batch_metadata": {"test": True}
    }
    update_data = {
        "name": "Updated Batch",
        "status": BatchStatus.FERMENTING,
        "actual_volume": 95.0,
        "end_date": datetime.utcnow() + timedelta(days=7),
        "notes": "Updated test batch",
        "batch_metadata": {"test": True, "updated": True}
    } 