from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class BatchDispatch(Base):
    __tablename__ = "batch_dispatches"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, unique=True, index=True, nullable=False)
    grower_id = Column(Integer, ForeignKey("growers.id"), nullable=False)
    produce_type = Column(String, nullable=False)
    varietal = Column(String, nullable=False)
    dispatch_date = Column(Date, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    
    # Relationship with grower (assuming you have a Grower model)
    grower = relationship("Grower", back_populates="batch_dispatches") 