from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.maintenance_log import MaintenanceLog
from app.schemas.maintenance_log import MaintenanceLogCreate, MaintenanceLogUpdate

class CRUDMaintenanceLog(CRUDBase[MaintenanceLog, MaintenanceLogCreate, MaintenanceLogUpdate]):
    def get_by_maintenance_id(self, db: Session, *, maintenance_id: int) -> List[MaintenanceLog]:
        return db.query(self.model).filter(self.model.maintenance_id == maintenance_id).all()

    def get_by_technician_id(self, db: Session, *, technician_id: int) -> List[MaintenanceLog]:
        return db.query(self.model).filter(self.model.technician_id == technician_id).all()

crud_maintenance_log = CRUDMaintenanceLog(MaintenanceLog) 