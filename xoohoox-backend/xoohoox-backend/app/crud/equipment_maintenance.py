from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.equipment_maintenance import EquipmentMaintenance
from app.schemas.equipment_maintenance import EquipmentMaintenanceCreate, EquipmentMaintenanceUpdate

class CRUDEquipmentMaintenance(CRUDBase[EquipmentMaintenance, EquipmentMaintenanceCreate, EquipmentMaintenanceUpdate]):
    def get_by_maintenance_id(self, db: Session, *, maintenance_id: int) -> Optional[EquipmentMaintenance]:
        """Get equipment maintenance record by maintenance ID."""
        return db.query(EquipmentMaintenance).filter(EquipmentMaintenance.maintenance_id == maintenance_id).first()
    
    def get_by_equipment_id(self, db: Session, *, equipment_id: int) -> List[EquipmentMaintenance]:
        """Get all maintenance records for a specific equipment."""
        return db.query(EquipmentMaintenance).filter(EquipmentMaintenance.equipment_id == equipment_id).all()

crud_equipment_maintenance = CRUDEquipmentMaintenance(EquipmentMaintenance) 