from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.equipment_maintenance import MaintenanceRecord
from app.schemas.equipment_maintenance import MaintenanceRecordCreate, MaintenanceRecordUpdate

class CRUDEquipmentMaintenance(CRUDBase[MaintenanceRecord, MaintenanceRecordCreate, MaintenanceRecordUpdate]):
    def get_by_equipment_id(self, db: Session, *, equipment_id: int) -> List[MaintenanceRecord]:
        return db.query(self.model).filter(self.model.equipment_id == equipment_id).all()

    def get_by_status(self, db: Session, *, status: str) -> List[MaintenanceRecord]:
        return db.query(self.model).filter(self.model.status == status).all()

    def get_by_maintenance_type(self, db: Session, *, maintenance_type: str) -> List[MaintenanceRecord]:
        return db.query(self.model).filter(self.model.maintenance_type == maintenance_type).all()

    def get_overdue_maintenance(self, db: Session) -> List[MaintenanceRecord]:
        from datetime import datetime
        return db.query(self.model).filter(
            self.model.next_maintenance_date <= datetime.utcnow(),
            self.model.status != "completed"
        ).all()

equipment_maintenance = CRUDEquipmentMaintenance(MaintenanceRecord) 