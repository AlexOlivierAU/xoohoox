from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.batch_dispatch import BatchDispatch
from app.schemas.batch_dispatch import BatchDispatchCreate, BatchDispatchUpdate

class CRUDBatchDispatch(CRUDBase[BatchDispatch, BatchDispatchCreate, BatchDispatchUpdate]):
    def get_by_batch_id(self, db: Session, *, batch_id: str) -> Optional[BatchDispatch]:
        return db.query(BatchDispatch).filter(BatchDispatch.batch_id == batch_id).first()
    
    def get_by_grower_id(self, db: Session, *, grower_id: int, skip: int = 0, limit: int = 100) -> List[BatchDispatch]:
        return db.query(BatchDispatch).filter(BatchDispatch.grower_id == grower_id).offset(skip).limit(limit).all()

batch_dispatch = CRUDBatchDispatch(BatchDispatch) 