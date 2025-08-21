from enum import Enum

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
    JUICER = "juicer"
    PASTEURIZER = "pasteurizer"
    FILTER = "filter"
    PUMP = "pump"
    TANK = "tank"
    CONVEYOR = "conveyor"
    PACKAGING = "packaging"
    OTHER = "other"

class EquipmentStatus(str, Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    REPAIR = "repair"
    DECOMMISSIONED = "decommissioned"
    OFFLINE = "offline"

class MaintenanceType(str, Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    ROUTINE = "routine"
    EMERGENCY = "emergency"

class MaintenanceStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

class MaintenancePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class QualityCheckType(str, Enum):
    PH = "ph"
    BRIX = "brix"
    ACIDITY = "acidity"
    ALCOHOL = "alcohol"
    TEMPERATURE = "temperature"
    VISUAL = "visual"
    TASTE = "taste"
    AROMA = "aroma"

class QualityTestType(str, Enum):
    PH = "ph"
    BRIX = "brix"
    TEMPERATURE = "temperature"
    ACIDITY = "acidity"
    TURBIDITY = "turbidity"
    COLOR = "color"
    VISCOSITY = "viscosity"
    MICROBIOLOGICAL = "microbiological"
    HEAVY_METALS = "heavy_metals"
    PESTICIDES = "pesticides"

class TestResult(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    PENDING = "pending"

class QualityGrade(str, Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    F = "f"

class ProcessStatus(str, Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class YeastStrain(str, Enum):
    STANDARD = "standard"
    CHAMPAGNE = "champagne"
    WINE = "wine"
    WILD = "wild"
    CUSTOM = "custom"

class InventoryType(str, Enum):
    RAW_MATERIAL = "raw_material"
    PACKAGING = "packaging"
    FINISHED_PRODUCT = "finished_product"
    SUPPLIES = "supplies"
    EQUIPMENT = "equipment"

class StockStatus(str, Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    ON_ORDER = "on_order"
    DISCONTINUED = "discontinued"

class AppleVariety(str, Enum):
    GRANNY_SMITH = "granny_smith"
    HONEYCRISP = "honeycrisp"
    FUJI = "fuji"
    GALA = "gala"
    RED_DELICIOUS = "red_delicious"
    GOLDEN_DELICIOUS = "golden_delicious"
    PINK_LADY = "pink_lady"
    BRAEBURN = "braeburn"
    JONAGOLD = "jonagold"
    MCINTOSH = "mcintosh"

class TransformationType(str, Enum):
    JUICING = "juicing"
    FERMENTATION = "fermentation"
    DISTILLATION = "distillation"
    FILTRATION = "filtration"
    PASTEURIZATION = "pasteurization"
    CONCENTRATION = "concentration"
    DEHYDRATION = "dehydration"

class JuiceProcessingType(str, Enum):
    COLD_PRESS = "cold_press"
    CENTRIFUGAL = "centrifugal"
    MASTICATING = "masticating"
    TRITURATING = "triturating"
    HYDRAULIC = "hydraulic"

class LogType(str, Enum):
    MAINTENANCE = "maintenance"
    REPAIR = "repair"
    INSPECTION = "inspection"
    CALIBRATION = "calibration"
    CLEANING = "cleaning"
    OTHER = "other" 