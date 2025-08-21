import pytest
from typing import Dict, Type
from sqlalchemy.orm import Session
from app.db.base_class import Base

class TestCRUDBase:
    model_class: Type[Base] = None
    create_data: Dict = {}
    update_data: Dict = {}

    def test_create(self, db_session: Session):
        assert self.model_class is not None, "model_class must be defined"
        assert self.create_data, "create_data must be defined"
        
        obj = self.model_class(**self.create_data)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        
        assert obj.id is not None
        for key, value in self.create_data.items():
            assert getattr(obj, key) == value

    def test_read(self, db_session: Session):
        assert self.model_class is not None, "model_class must be defined"
        assert self.create_data, "create_data must be defined"
        
        obj = self.model_class(**self.create_data)
        db_session.add(obj)
        db_session.commit()
        
        db_obj = db_session.query(self.model_class).filter_by(id=obj.id).first()
        assert db_obj is not None
        for key, value in self.create_data.items():
            assert getattr(db_obj, key) == value

    def test_update(self, db_session: Session):
        assert self.model_class is not None, "model_class must be defined"
        assert self.create_data, "create_data must be defined"
        assert self.update_data, "update_data must be defined"
        
        obj = self.model_class(**self.create_data)
        db_session.add(obj)
        db_session.commit()
        
        for key, value in self.update_data.items():
            setattr(obj, key, value)
        db_session.commit()
        db_session.refresh(obj)
        
        for key, value in self.update_data.items():
            assert getattr(obj, key) == value

    def test_delete(self, db_session: Session):
        assert self.model_class is not None, "model_class must be defined"
        assert self.create_data, "create_data must be defined"
        
        obj = self.model_class(**self.create_data)
        db_session.add(obj)
        db_session.commit()
        
        db_session.delete(obj)
        db_session.commit()
        
        db_obj = db_session.query(self.model_class).filter_by(id=obj.id).first()
        assert db_obj is None 