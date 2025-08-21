from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.batch_tracking import BatchTracking
from app.models.enums import BatchStatus, QualityGrade
from app.schemas.batch_tracking import (
    BatchTrackingCreate,
    BatchTrackingUpdate,
    StartProduction,
    CompleteProduction,
    QualityCheckResult,
    ReportIssue,
    TakeCorrectiveAction,
)

class CRUDBatchTracking(CRUDBase[BatchTracking, BatchTrackingCreate, BatchTrackingUpdate]):
    def get_by_batch_id(self, db: Session, *, batch_id: str) -> Optional[BatchTracking]:
        return db.query(BatchTracking).filter(BatchTracking.batch_id == batch_id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        juice_type: Optional[str] = None,
        status: Optional[BatchStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[BatchTracking]:
        query = db.query(BatchTracking)
        
        if juice_type:
            query = query.filter(BatchTracking.juice_type == juice_type)
        if status:
            query = query.filter(BatchTracking.status == status)
        if start_date:
            query = query.filter(BatchTracking.production_date >= start_date)
        if end_date:
            query = query.filter(BatchTracking.production_date <= end_date)
        
        return query.offset(skip).limit(limit).all()
    
    def start_production(
        self,
        db: Session,
        *,
        batch_id: str,
        data: StartProduction,
    ) -> BatchTracking:
        batch = self.get_by_batch_id(db, batch_id=batch_id)
        if not batch:
            return None
        
        if batch.status != BatchStatus.PLANNED:
            raise ValueError("Can only start production for planned batches")
        
        update_data = {
            "status": BatchStatus.IN_PRODUCTION,
            "actual_ingredients": data.actual_ingredients,
            "temperature": data.temperature,
            "updated_by": data.started_by,
        }
        
        return self.update(db, db_obj=batch, obj_in=update_data)
    
    def complete_production(
        self,
        db: Session,
        *,
        batch_id: str,
        data: CompleteProduction,
    ) -> BatchTracking:
        batch = self.get_by_batch_id(db, batch_id=batch_id)
        if not batch:
            return None
        
        if batch.status != BatchStatus.IN_PRODUCTION:
            raise ValueError("Can only complete batches that are in production")
        
        update_data = {
            "status": BatchStatus.QUALITY_CHECK,
            "actual_quantity": data.actual_quantity,
            "processing_time": data.processing_time,
            "completion_date": datetime.utcnow(),
            "updated_by": data.completed_by,
        }
        
        return self.update(db, db_obj=batch, obj_in=update_data)
    
    def record_quality_check(
        self,
        db: Session,
        *,
        batch_id: str,
        data: QualityCheckResult,
    ) -> BatchTracking:
        batch = self.get_by_batch_id(db, batch_id=batch_id)
        if not batch:
            return None
        
        if batch.status != BatchStatus.QUALITY_CHECK:
            raise ValueError("Can only record quality checks for batches in quality check status")
        
        update_data = {
            "status": BatchStatus.COMPLETED if data.quality_grade != QualityGrade.REJECTED else BatchStatus.REJECTED,
            "quality_grade": data.quality_grade,
            "quality_checks": data.quality_checks,
            "updated_by": data.checked_by,
        }
        
        return self.update(db, db_obj=batch, obj_in=update_data)
    
    def report_issue(
        self,
        db: Session,
        *,
        batch_id: str,
        data: ReportIssue,
    ) -> BatchTracking:
        batch = self.get_by_batch_id(db, batch_id=batch_id)
        if not batch:
            return None
        
        current_issues = batch.issues or []
        current_issues.append(data.issue)
        
        update_data = {
            "issues": current_issues,
            "updated_by": data.reported_by,
        }
        
        return self.update(db, db_obj=batch, obj_in=update_data)
    
    def take_corrective_action(
        self,
        db: Session,
        *,
        batch_id: str,
        data: TakeCorrectiveAction,
    ) -> BatchTracking:
        batch = self.get_by_batch_id(db, batch_id=batch_id)
        if not batch:
            return None
        
        current_actions = batch.corrective_actions or []
        current_actions.append(data.action)
        
        update_data = {
            "corrective_actions": current_actions,
            "updated_by": data.taken_by,
        }
        
        return self.update(db, db_obj=batch, obj_in=update_data)

batch_tracking = CRUDBatchTracking(BatchTracking) 