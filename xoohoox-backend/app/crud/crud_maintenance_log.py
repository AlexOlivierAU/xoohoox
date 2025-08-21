from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.maintenance_log import MaintenanceLog
from app.schemas.maintenance_log import MaintenanceLogCreate, MaintenanceLogUpdate

class CRUDMaintenanceLog(CRUDBase[MaintenanceLog, MaintenanceLogCreate, MaintenanceLogUpdate]):
    def get_by_maintenance(
        self, db: Session, *, maintenance_id: int, skip: int = 0, limit: int = 100
    ) -> List[MaintenanceLog]:
        return (
            db.query(self.model)
            .filter(MaintenanceLog.maintenance_id == maintenance_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_technician(
        self, db: Session, *, technician_id: int, skip: int = 0, limit: int = 100
    ) -> List[MaintenanceLog]:
        return (
            db.query(self.model)
            .filter(MaintenanceLog.technician_id == technician_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

maintenance_log = CRUDMaintenanceLog(MaintenanceLog) 