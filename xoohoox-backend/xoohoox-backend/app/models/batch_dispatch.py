from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class BatchDispatch(BaseModel):
    __tablename__ = "batch_dispatches"
    batch_id = Column(String, unique=True, index=True, nullable=False)
    grower_id = Column(Integer, nullable=False)
    produce_type = Column(String, nullable=False)
    varietal = Column(String, nullable=False)
    dispatch_date = Column(Date, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    
    # Relationship with grower (commented out until Grower model is created)
    # grower = relationship("Grower", back_populates="batch_dispatches") 