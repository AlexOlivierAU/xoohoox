from enum import Enum, auto

class BatchStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FERMENTING = "fermenting"
    DISTILLING = "distilling"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class FruitType(str, Enum):
    APPLE = "apple"
    PEAR = "pear"
    GRAPE = "grape"
    MIXED = "mixed"
    OTHER = "other"

class JuiceType(str, Enum):
    FRESH = "fresh"
    CONCENTRATE = "concentrate"
    BLEND = "blend"
    CUSTOM = "custom"

class EquipmentType(str, Enum):
    PRESS = "press"
    FILTER = "filter"
    PUMP = "pump"
    TANK = "tank"
    FERMENTOR = "fermentor"
    STILL = "still"
    SENSOR = "sensor"
    HVAC = "hvac"
    PACKAGING = "packaging"
    OTHER = "other"

class EquipmentStatus(str, Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    REPAIR = "repair"
    DECOMMISSIONED = "decommissioned"
    OFFLINE = "offline"

class MaintenanceType(str, Enum):
    """Types of maintenance operations"""
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    ROUTINE = "routine"
    EMERGENCY = "emergency"
    CALIBRATION = "calibration"
    INSPECTION = "inspection"

class MaintenanceStatus(str, Enum):
    """Status of maintenance operations"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"
    PENDING_PARTS = "pending_parts"
    PENDING_APPROVAL = "pending_approval"

class QualityTestType(str, Enum):
    PH = "ph"
    BRIX = "brix"
    TEMPERATURE = "temperature"
    ALCOHOL_CONTENT = "alcohol_content"
    ACIDITY = "acidity"
    SUGAR_CONTENT = "sugar_content"
    CLARITY = "clarity"
    COLOR = "color"
    AROMA = "aroma"
    TASTE = "taste"

class TestResult(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    PENDING = "pending"

class ProcessStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TransformationType(str, Enum):
    JUICING = "juicing"
    FERMENTATION = "fermentation"
    DISTILLATION = "distillation"
    BLENDING = "blending"
    AGING = "aging"
    BOTTLING = "bottling"

class JuiceProcessingType(str, Enum):
    COLD_PRESS = "cold_press"
    CENTRIFUGAL = "centrifugal"
    MASTICATING = "masticating"
    HYDRAULIC_PRESS = "hydraulic_press"
    STEAM_EXTRACTION = "steam_extraction"

class LogType(str, Enum):
    """Types of maintenance log entries"""
    INSPECTION = "inspection"
    REPAIR = "repair"
    SERVICE = "service"
    CALIBRATION = "calibration"
    CLEANING = "cleaning"
    PARTS_REPLACEMENT = "parts_replacement"
    TESTING = "testing"
    VERIFICATION = "verification"
    OTHER = "other" 