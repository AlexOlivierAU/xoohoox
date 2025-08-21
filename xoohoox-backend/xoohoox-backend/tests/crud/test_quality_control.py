import pytest
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from app.models.quality_control import QualityControl
from app.models.enums import QualityTestType, TestResult
from tests.crud.test_crud import TestCRUDBase

class TestQualityControlCRUD(TestCRUDBase):
    """Test CRUD operations for QualityControl model."""
    
    @pytest.fixture
    def quality_control_data(self, test_batch) -> Dict[str, Any]:
        return {
            "batch_id": test_batch.id,
            "test_type": QualityTestType.PH,
            "test_value": 3.5,
            "test_result": TestResult.PASS,
            "test_date": datetime.utcnow(),
            "notes": "Initial quality test"
        }
    
    @pytest.fixture
    def quality_control_update_data(self) -> Dict[str, Any]:
        return {
            "test_value": 3.8,
            "test_result": TestResult.FAIL,
            "notes": "Updated test results"
        }
    
    @pytest.fixture
    def test_quality_control(self, db_session: Session, quality_control_data: Dict[str, Any]) -> QualityControl:
        """Create a test quality control record."""
        quality_control = QualityControl(**quality_control_data)
        db_session.add(quality_control)
        db_session.commit()
        db_session.refresh(quality_control)
        return quality_control
    
    def test_create_quality_control(self, db_session: Session, quality_control_data: Dict[str, Any]) -> None:
        self.test_create(db_session, QualityControl, quality_control_data)
    
    def test_read_quality_control(self, db_session: Session, test_quality_control: QualityControl) -> None:
        self.test_read(db_session, QualityControl, test_quality_control)
    
    def test_update_quality_control(self, db_session: Session, test_quality_control: QualityControl, quality_control_update_data: Dict[str, Any]) -> None:
        self.test_update(db_session, QualityControl, test_quality_control, quality_control_update_data)
    
    def test_delete_quality_control(self, db_session: Session, test_quality_control: QualityControl) -> None:
        self.test_delete(db_session, QualityControl, test_quality_control)
    
    def test_quality_control_batch_relationship(self, db_session: Session, test_quality_control: QualityControl, test_batch) -> None:
        """Test the relationship between QualityControl and BatchTracking."""
        assert test_quality_control.batch_id == test_batch.id
        assert test_quality_control.batch == test_batch 