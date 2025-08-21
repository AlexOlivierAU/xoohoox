from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.enums import TransformationType, ProcessStatus, JuiceProcessingType

class TransformationStage(Base):
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), nullable=False)
    stage_type = Column(SQLAlchemyEnum(TransformationType, name="transformation_type"), nullable=False)
    status = Column(SQLAlchemyEnum(ProcessStatus, name="process_status"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    batch = relationship("Batch", back_populates="transformation_stages")

    def __repr__(self):
        return f"<TransformationStage(id={self.id}, batch_id={self.batch_id}, type={self.stage_type})>" 