from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.maintenance_log import MaintenanceLog
from app.schemas.maintenance_log import MaintenanceLogCreate, MaintenanceLogUpdate

class CRUDMaintenanceLog(CRUDBase[MaintenanceLog, MaintenanceLogCreate, MaintenanceLogUpdate]):
    def get_by_maintenance_id(self, db: Session, *, maintenance_id: int) -> List[MaintenanceLog]:
        """Get all log entries for a specific maintenance record."""
        return db.query(MaintenanceLog).filter(MaintenanceLog.maintenance_id == maintenance_id).all()
    
    def get_by_performed_by(self, db: Session, *, performed_by: str) -> List[MaintenanceLog]:
        """Get all log entries performed by a specific person."""
        return db.query(MaintenanceLog).filter(MaintenanceLog.performed_by == performed_by).all()

maintenance_log = CRUDMaintenanceLog(MaintenanceLog) 