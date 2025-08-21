import pytest
from datetime import datetime
from app.models.inventory_management import InventoryManagement
from app.models.enums import InventoryType, StockStatus, FruitType

def test_inventory_creation():
    """Test creating an inventory record with valid data."""
    inventory = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=1000.0,
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0,
        unit_cost=2.50,
        location="Warehouse A",
        supplier_id=1
    )
    
    assert inventory.item_name == "Honeycrisp Apples"
    assert inventory.item_type == InventoryType.RAW_MATERIAL
    assert inventory.fruit_type == FruitType.APPLE
    assert inventory.quantity == 1000.0
    assert inventory.unit == "kg"
    assert inventory.minimum_stock_level == 100.0
    assert inventory.maximum_stock_level == 2000.0
    assert inventory.reorder_point == 500.0
    assert inventory.unit_cost == 2.50
    assert inventory.location == "Warehouse A"
    assert inventory.supplier_id == 1

def test_inventory_defaults():
    """Test default values for inventory fields."""
    inventory = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=1000.0,
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0
    )
    
    assert inventory.unit_cost == 0.0  # Should default to 0
    assert inventory.location is None
    assert inventory.supplier_id is None
    assert inventory.notes is None

def test_inventory_representation():
    """Test string representation of InventoryManagement model."""
    inventory = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=1000.0,
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0
    )
    
    str_repr = str(inventory)
    assert "InventoryManagement" in str_repr
    assert "Honeycrisp Apples" in str_repr
    assert "1000.0 kg" in str_repr

def test_inventory_to_dict():
    """Test the to_dict method of InventoryManagement model."""
    inventory = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=1000.0,
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0,
        unit_cost=2.50,
        location="Warehouse A",
        supplier_id=1
    )
    
    inv_dict = inventory.to_dict()
    
    assert inv_dict['item_name'] == "Honeycrisp Apples"
    assert inv_dict['item_type'] == InventoryType.RAW_MATERIAL.value
    assert inv_dict['fruit_type'] == FruitType.APPLE.value
    assert inv_dict['quantity'] == 1000.0
    assert inv_dict['unit'] == "kg"
    assert inv_dict['minimum_stock_level'] == 100.0
    assert inv_dict['maximum_stock_level'] == 2000.0
    assert inv_dict['reorder_point'] == 500.0
    assert inv_dict['unit_cost'] == 2.50
    assert inv_dict['location'] == "Warehouse A"
    assert inv_dict['supplier_id'] == 1

def test_inventory_validation():
    """Test inventory validation rules."""
    # Test invalid quantity (negative)
    with pytest.raises(ValueError):
        InventoryManagement(
            item_name="Honeycrisp Apples",
            item_type=InventoryType.RAW_MATERIAL,
            fruit_type=FruitType.APPLE,
            quantity=-100.0,  # Negative quantity
            unit="kg",
            minimum_stock_level=100.0,
            maximum_stock_level=2000.0,
            reorder_point=500.0
        )
    
    # Test invalid stock levels (min > max)
    with pytest.raises(ValueError):
        InventoryManagement(
            item_name="Honeycrisp Apples",
            item_type=InventoryType.RAW_MATERIAL,
            fruit_type=FruitType.APPLE,
            quantity=1000.0,
            unit="kg",
            minimum_stock_level=2000.0,  # Greater than max
            maximum_stock_level=1000.0,
            reorder_point=500.0
        )
    
    # Test invalid reorder point (outside min-max range)
    with pytest.raises(ValueError):
        InventoryManagement(
            item_name="Honeycrisp Apples",
            item_type=InventoryType.RAW_MATERIAL,
            fruit_type=FruitType.APPLE,
            quantity=1000.0,
            unit="kg",
            minimum_stock_level=100.0,
            maximum_stock_level=2000.0,
            reorder_point=2500.0  # Greater than max
        )

def test_inventory_stock_status():
    """Test stock status calculation based on quantity levels."""
    # Test IN_STOCK status
    inventory_normal = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=1000.0,
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0
    )
    assert inventory_normal.stock_status == StockStatus.IN_STOCK
    
    # Test LOW_STOCK status
    inventory_low = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=300.0,  # Below reorder point
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0
    )
    assert inventory_low.stock_status == StockStatus.LOW_STOCK
    
    # Test OUT_OF_STOCK status
    inventory_out = InventoryManagement(
        item_name="Honeycrisp Apples",
        item_type=InventoryType.RAW_MATERIAL,
        fruit_type=FruitType.APPLE,
        quantity=50.0,  # Below minimum
        unit="kg",
        minimum_stock_level=100.0,
        maximum_stock_level=2000.0,
        reorder_point=500.0
    )
    assert inventory_out.stock_status == StockStatus.OUT_OF_STOCK 