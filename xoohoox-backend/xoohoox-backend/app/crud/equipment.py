from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate

class CRUDEquipment(CRUDBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_type(self, db: Session, *, equipment_type: str) -> List[Equipment]:
        """Get all equipment of a specific type."""
        return db.query(Equipment).filter(Equipment.type == equipment_type).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Equipment]:
        """Get all equipment with a specific status."""
        return db.query(Equipment).filter(Equipment.status == status).all()
    
    def get_critical_equipment(self, db: Session) -> List[Equipment]:
        """Get all critical equipment."""
        return db.query(Equipment).filter(Equipment.is_critical == True).all()

equipment = CRUDEquipment(Equipment)
