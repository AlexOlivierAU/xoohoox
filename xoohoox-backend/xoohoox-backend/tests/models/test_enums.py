import pytest
from enum import Enum
from app.models.enums import (
    FruitType,
    AppleVariety,
    BatchStatus,
    EquipmentStatus,
    MaintenanceType,
    MaintenancePriority,
    QualityTestType,
    TestResult,
    InventoryType,
    StockStatus
)

def test_fruit_type_values():
    """Test that FruitType enum has the expected values."""
    assert FruitType.APPLE.value == "apple"
    assert FruitType.PEAR.value == "pear"
    assert FruitType.GRAPE.value == "grape"
    assert FruitType.MIXED.value == "mixed"

def test_apple_variety_values():
    """Test that AppleVariety enum has the expected values."""
    assert AppleVariety.HONEYCRISP.value == "honeycrisp"
    assert AppleVariety.GRANNY_SMITH.value == "granny_smith"
    assert AppleVariety.FUJI.value == "fuji"
    assert AppleVariety.GALA.value == "gala"
    assert AppleVariety.RED_DELICIOUS.value == "red_delicious"
    assert AppleVariety.GOLDEN_DELICIOUS.value == "golden_delicious"
    assert AppleVariety.MIXED.value == "mixed"

def test_batch_status_values():
    """Test that BatchStatus enum has the expected values and order."""
    assert BatchStatus.PLANNED.value == "planned"
    assert BatchStatus.IN_PROGRESS.value == "in_progress"
    assert BatchStatus.COMPLETED.value == "completed"
    assert BatchStatus.CANCELLED.value == "cancelled"
    assert BatchStatus.ON_HOLD.value == "on_hold"
    
    # Test that statuses are ordered correctly
    assert BatchStatus.PLANNED < BatchStatus.IN_PROGRESS
    assert BatchStatus.IN_PROGRESS < BatchStatus.COMPLETED

def test_equipment_status_values():
    """Test that EquipmentStatus enum has the expected values."""
    assert EquipmentStatus.OPERATIONAL.value == "operational"
    assert EquipmentStatus.MAINTENANCE.value == "maintenance"
    assert EquipmentStatus.REPAIR.value == "repair"
    assert EquipmentStatus.OUT_OF_SERVICE.value == "out_of_service"

def test_maintenance_type_values():
    """Test that MaintenanceType enum has the expected values."""
    assert MaintenanceType.PREVENTIVE.value == "preventive"
    assert MaintenanceType.CORRECTIVE.value == "corrective"
    assert MaintenanceType.PREDICTIVE.value == "predictive"
    assert MaintenanceType.EMERGENCY.value == "emergency"

def test_maintenance_priority_values():
    """Test that MaintenancePriority enum has the expected values and order."""
    assert MaintenancePriority.LOW.value == "low"
    assert MaintenancePriority.MEDIUM.value == "medium"
    assert MaintenancePriority.HIGH.value == "high"
    assert MaintenancePriority.CRITICAL.value == "critical"
    
    # Test priority ordering
    assert MaintenancePriority.LOW < MaintenancePriority.MEDIUM
    assert MaintenancePriority.MEDIUM < MaintenancePriority.HIGH
    assert MaintenancePriority.HIGH < MaintenancePriority.CRITICAL

def test_quality_test_type_values():
    """Test that QualityTestType enum has the expected values."""
    assert QualityTestType.PH.value == "ph"
    assert QualityTestType.BRIX.value == "brix"
    assert QualityTestType.TEMPERATURE.value == "temperature"
    assert QualityTestType.ALCOHOL_CONTENT.value == "alcohol_content"
    assert QualityTestType.ACIDITY.value == "acidity"
    assert QualityTestType.CLARITY.value == "clarity"

def test_test_result_values():
    """Test that TestResult enum has the expected values."""
    assert TestResult.PASS.value == "pass"
    assert TestResult.FAIL.value == "fail"
    assert TestResult.PENDING.value == "pending"
    assert TestResult.INCONCLUSIVE.value == "inconclusive"

def test_inventory_type_values():
    """Test that InventoryType enum has the expected values."""
    assert InventoryType.RAW_MATERIAL.value == "raw_material"
    assert InventoryType.FINISHED_PRODUCT.value == "finished_product"
    assert InventoryType.PACKAGING.value == "packaging"
    assert InventoryType.SUPPLIES.value == "supplies"

def test_stock_status_values():
    """Test that StockStatus enum has the expected values."""
    assert StockStatus.IN_STOCK.value == "in_stock"
    assert StockStatus.LOW_STOCK.value == "low_stock"
    assert StockStatus.OUT_OF_STOCK.value == "out_of_stock"
    assert StockStatus.DISCONTINUED.value == "discontinued"

def test_enum_uniqueness():
    """Test that all enum values are unique within their respective enums."""
    def check_enum_uniqueness(enum_class):
        values = [member.value for member in enum_class]
        assert len(values) == len(set(values)), f"Duplicate values found in {enum_class.__name__}"
    
    enums = [
        FruitType,
        AppleVariety,
        BatchStatus,
        EquipmentStatus,
        MaintenanceType,
        MaintenancePriority,
        QualityTestType,
        TestResult,
        InventoryType,
        StockStatus
    ]
    
    for enum in enums:
        check_enum_uniqueness(enum)

def test_enum_value_types():
    """Test that all enum values are strings."""
    def check_enum_value_types(enum_class):
        for member in enum_class:
            assert isinstance(member.value, str), f"Non-string value found in {enum_class.__name__}: {member.name}"
    
    enums = [
        FruitType,
        AppleVariety,
        BatchStatus,
        EquipmentStatus,
        MaintenanceType,
        MaintenancePriority,
        QualityTestType,
        TestResult,
        InventoryType,
        StockStatus
    ]
    
    for enum in enums:
        check_enum_value_types(enum) 