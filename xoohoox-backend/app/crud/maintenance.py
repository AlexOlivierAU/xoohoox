from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.maintenance import Maintenance
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate

class CRUDMaintenance(CRUDBase[Maintenance, MaintenanceCreate, MaintenanceUpdate]):
    def get_by_equipment_id(self, db: Session, *, equipment_id: int) -> List[Maintenance]:
        return db.query(self.model).filter(self.model.equipment_id == equipment_id).all()

    def get_by_status(self, db: Session, *, status: str) -> List[Maintenance]:
        return db.query(self.model).filter(self.model.status == status).all()

    def get_by_priority(self, db: Session, *, priority: str) -> List[Maintenance]:
        return db.query(self.model).filter(self.model.priority == priority).all()

    def get_by_maintenance_type(self, db: Session, *, maintenance_type: str) -> List[Maintenance]:
        return db.query(self.model).filter(self.model.maintenance_type == maintenance_type).all()

crud_maintenance = CRUDMaintenance(Maintenance) 