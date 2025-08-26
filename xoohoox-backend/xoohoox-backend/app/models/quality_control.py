from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import QualityCheckType, TestResult

class QualityControl(BaseModel):
    __tablename__ = "quality_control"

    test_id = Column(String, unique=True, index=True, nullable=False)
    batch_id = Column(String, ForeignKey("batch_tracking.batch_id"), nullable=False)
    juicing_input_id = Column(Integer, ForeignKey("juicing_input_log.id"), nullable=True)
    test_type = Column(SQLEnum(QualityCheckType), nullable=False)
    test_date = Column(DateTime(timezone=True), nullable=False)
    test_name = Column(String, nullable=False)
    test_method = Column(String, nullable=False)
    test_parameters = Column(String)
    expected_range_min = Column(Float)
    expected_range_max = Column(Float)
    actual_value = Column(Float)
    unit_of_measure = Column(String, nullable=False)
    result = Column(SQLEnum(TestResult), nullable=False, default=TestResult.PENDING)
    tester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    equipment_used = Column(String)
    temperature_c = Column(Float)
    humidity_percent = Column(Float)
    notes = Column(String)
    corrective_actions = Column(String)
    retest_required = Column(Boolean, default=False)

    # Relationships
    batch = relationship("BatchTracking", back_populates="quality_records", lazy="joined")
    # tester = relationship("User", backref="quality_tests", lazy="joined")  # Temporarily commented out - User model not ready
    # juicing_input = relationship("JuicingInputLog", back_populates="quality_checks", lazy="joined")  # Temporarily commented out 