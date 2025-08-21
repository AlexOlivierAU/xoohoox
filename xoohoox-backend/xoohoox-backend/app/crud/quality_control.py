from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.quality_control import QualityControl
from app.schemas.quality_control import QualityControlCreate, QualityControlUpdate, TestResult

class CRUDQualityControl(CRUDBase[QualityControl, QualityControlCreate, QualityControlUpdate]):
    def get_by_test_id(self, db: Session, *, test_id: str) -> Optional[QualityControl]:
        return db.query(QualityControl).filter(QualityControl.test_id == test_id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        batch_id: Optional[str] = None,
        result: Optional[TestResult] = None
    ) -> List[QualityControl]:
        query = db.query(QualityControl)
        if batch_id:
            query = query.filter(QualityControl.batch_id == batch_id)
        if result:
            query = query.filter(QualityControl.result == result)
        return query.offset(skip).limit(limit).all()
    
    def count(
        self,
        db: Session,
        *,
        batch_id: Optional[str] = None,
        result: Optional[TestResult] = None
    ) -> int:
        query = db.query(QualityControl)
        if batch_id:
            query = query.filter(QualityControl.batch_id == batch_id)
        if result:
            query = query.filter(QualityControl.result == result)
        return query.count()
    
    def create(self, db: Session, *, obj_in: QualityControlCreate) -> QualityControl:
        db_obj = QualityControl(
            test_id=obj_in.test_id,
            batch_id=obj_in.batch_id,
            test_type=obj_in.test_type,
            test_date=obj_in.test_date,
            test_name=obj_in.test_name,
            test_method=obj_in.test_method,
            test_parameters=obj_in.test_parameters,
            expected_range_min=obj_in.expected_range_min,
            expected_range_max=obj_in.expected_range_max,
            actual_value=obj_in.actual_value,
            unit_of_measure=obj_in.unit_of_measure,
            result=obj_in.result,
            tester_id=obj_in.tester_id,
            equipment_used=obj_in.equipment_used,
            temperature_c=obj_in.temperature_c,
            humidity_percent=obj_in.humidity_percent,
            notes=obj_in.notes,
            corrective_actions=obj_in.corrective_actions,
            retest_required=obj_in.retest_required
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: QualityControl,
        obj_in: Union[QualityControlUpdate, Dict[str, Any]]
    ) -> QualityControl:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Validate actual value against expected range if provided
        if 'actual_value' in update_data:
            actual_value = update_data['actual_value']
            min_val = db_obj.expected_range_min
            max_val = db_obj.expected_range_max
            
            if min_val is not None and max_val is not None and actual_value is not None:
                if min_val <= actual_value <= max_val:
                    update_data['result'] = TestResult.PASS
                else:
                    update_data['result'] = TestResult.FAIL
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def verify_test(self, db: Session, *, db_obj: QualityControl) -> QualityControl:
        # Automatically determine test result based on actual value and expected range
        if db_obj.actual_value is not None and db_obj.expected_range_min is not None and db_obj.expected_range_max is not None:
            if db_obj.expected_range_min <= db_obj.actual_value <= db_obj.expected_range_max:
                db_obj.result = TestResult.PASS
            else:
                db_obj.result = TestResult.FAIL
        else:
            db_obj.result = TestResult.INCONCLUSIVE
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def request_retest(self, db: Session, *, db_obj: QualityControl) -> QualityControl:
        db_obj.retest_required = True
        db_obj.notes = f"{db_obj.notes}\nRetest requested at {datetime.utcnow()}" if db_obj.notes else f"Retest requested at {datetime.utcnow()}"
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

quality_control = CRUDQualityControl(QualityControl) 