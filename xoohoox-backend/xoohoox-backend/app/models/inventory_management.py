from sqlalchemy import Column, String, DateTime, Float, Text, Enum, Integer, Boolean
from app.models.base import BaseModel
import enum

class ItemType(str, enum.Enum):
    RAW_MATERIAL = "Raw Material"
    PACKAGING = "Packaging"
    FINISHED_PRODUCT = "Finished Product"
    CLEANING_SUPPLY = "Cleaning Supply"
    SPARE_PART = "Spare Part"
    OTHER = "Other"

class StorageCondition(str, enum.Enum):
    AMBIENT = "Ambient"
    REFRIGERATED = "Refrigerated"
    FROZEN = "Frozen"
    CONTROLLED = "Controlled"

class InventoryStatus(str, enum.Enum):
    IN_STOCK = "In Stock"
    LOW_STOCK = "Low Stock"
    OUT_OF_STOCK = "Out of Stock"
    EXPIRED = "Expired"
    RESERVED = "Reserved"
    DISCONTINUED = "Discontinued"

class InventoryManagement(BaseModel):
    """Model for tracking inventory items and stock levels"""
    __tablename__ = "inventory_management"

    item_id = Column(String(10), unique=True, index=True, nullable=False)
    item_name = Column(String(100), nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    description = Column(Text, nullable=True)
    sku = Column(String(50), unique=True, nullable=True)
    barcode = Column(String(50), unique=True, nullable=True)
    unit_of_measure = Column(String(20), nullable=False)
    quantity_in_stock = Column(Float, default=0, nullable=False)
    minimum_stock_level = Column(Float, nullable=False)
    reorder_point = Column(Float, nullable=False)
    maximum_stock_level = Column(Float, nullable=True)
    storage_location = Column(String(50), nullable=False)
    storage_condition = Column(Enum(StorageCondition), nullable=False)
    status = Column(Enum(InventoryStatus), default=InventoryStatus.IN_STOCK, nullable=False)
    supplier_id = Column(String(50), nullable=True)
    supplier_name = Column(String(100), nullable=True)
    unit_cost = Column(Float, nullable=True)
    last_ordered_date = Column(DateTime, nullable=True)
    last_received_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    lot_number = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Additional tracking fields
    total_received = Column(Float, default=0, nullable=False)
    total_issued = Column(Float, default=0, nullable=False)
    total_adjusted = Column(Float, default=0, nullable=False)  # For inventory adjustments
    last_count_date = Column(DateTime, nullable=True)
    last_count_quantity = Column(Float, nullable=True) 