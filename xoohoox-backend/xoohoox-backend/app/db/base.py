from app.db.base_class import Base

# Import all models here so they are registered with SQLAlchemy
from app.models.user import User
from app.models.batch_tracking import BatchTracking
from app.models.batch_dispatch import BatchDispatch
from app.models.batch import Batch
from app.models.yeast_strain import YeastStrain
from app.models.evaluation import Evaluation
from app.models.fermentation_log import FermentationLog
from app.models.juicing_log import JuicingLog
from app.models.farm import Farm
from app.models.upscale import UpscaleRun
from app.models.equipment import Equipment
from app.models.maintenance_log import MaintenanceLog
from app.models.equipment_maintenance import EquipmentMaintenance
from app.models.transformation import TransformationStage, JuicingResults, FermentationResults
from app.models.juicing_input_log import JuicingInputLog
from app.models.inventory_management import InventoryManagement
from app.models.quality_control import QualityControl
from app.models.fermentation_trial import FermentationTrial 