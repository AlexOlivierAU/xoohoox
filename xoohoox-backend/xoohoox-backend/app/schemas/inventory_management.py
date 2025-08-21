from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class ItemType(str, Enum):
    RAW_MATERIAL = "RAW_MATERIAL"
    PACKAGING = "PACKAGING"
    FINISHED_PRODUCT = "FINISHED_PRODUCT"
    CLEANING_SUPPLY = "CLEANING_SUPPLY"
    SPARE_PART = "SPARE_PART"
    OTHER = "OTHER"

class StorageCondition(str, Enum):
    AMBIENT = "AMBIENT"
    REFRIGERATED = "REFRIGERATED"
    FROZEN = "FROZEN"
    CONTROLLED = "CONTROLLED"

class InventoryStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    EXPIRED = "EXPIRED"
    RESERVED = "RESERVED"
    DISCONTINUED = "DISCONTINUED"

# Base schema with common attributes
class InventoryManagementBase(BaseModel):
    item_id: str = Field(..., description="Unique identifier for the inventory item")
    item_name: str = Field(..., description="Name of the inventory item")
    item_type: ItemType = Field(..., description="Type of inventory item")
    description: str = Field(..., description="Description of the inventory item")
    sku: str = Field(..., description="Stock Keeping Unit")
    barcode: Optional[str] = Field(None, description="Barcode of the inventory item")
    unit_of_measure: str = Field(..., description="Unit of measurement")
    quantity_in_stock: float = Field(..., ge=0, description="Current quantity in stock")
    minimum_stock_level: float = Field(..., ge=0, description="Minimum stock level before reordering")
    reorder_point: float = Field(..., ge=0, description="Point at which to reorder")
    maximum_stock_level: float = Field(..., ge=0, description="Maximum stock level")
    storage_location: str = Field(..., description="Location where the item is stored")
    storage_condition: StorageCondition = Field(..., description="Storage condition required")
    status: InventoryStatus = Field(..., description="Current status of the inventory item")
    supplier_id: Optional[str] = Field(None, description="ID of the supplier")
    supplier_name: Optional[str] = Field(None, description="Name of the supplier")
    unit_cost: float = Field(..., gt=0, description="Cost per unit")
    last_ordered_date: Optional[datetime] = Field(None, description="Date when the item was last ordered")
    last_received_date: Optional[datetime] = Field(None, description="Date when the item was last received")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date of the item")
    lot_number: Optional[str] = Field(None, description="Lot number of the item")
    is_active: bool = Field(True, description="Whether the item is active")
    notes: Optional[str] = Field(None, description="Additional notes about the item")
    total_received: float = Field(0, ge=0, description="Total quantity received")
    total_issued: float = Field(0, ge=0, description="Total quantity issued")
    total_adjusted: float = Field(0, description="Total quantity adjusted")
    last_count_date: Optional[datetime] = Field(None, description="Date of last physical count")
    last_count_quantity: Optional[float] = Field(None, ge=0, description="Quantity from last physical count")

    @validator('maximum_stock_level')
    def validate_maximum_stock_level(cls, v, values):
        if 'minimum_stock_level' in values and v < values['minimum_stock_level']:
            raise ValueError("Maximum stock level must be greater than minimum stock level")
        return v

    @validator('reorder_point')
    def validate_reorder_point(cls, v, values):
        if 'minimum_stock_level' in values and v < values['minimum_stock_level']:
            raise ValueError("Reorder point must be greater than or equal to minimum stock level")
        if 'maximum_stock_level' in values and v > values['maximum_stock_level']:
            raise ValueError("Reorder point must be less than or equal to maximum stock level")
        return v

# Schema for creating a new inventory item
class InventoryManagementCreate(InventoryManagementBase):
    pass

# Schema for updating an existing inventory item
class InventoryManagementUpdate(BaseModel):
    item_name: Optional[str] = None
    item_type: Optional[ItemType] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    unit_of_measure: Optional[str] = None
    quantity_in_stock: Optional[float] = Field(None, ge=0)
    minimum_stock_level: Optional[float] = Field(None, ge=0)
    reorder_point: Optional[float] = Field(None, ge=0)
    maximum_stock_level: Optional[float] = Field(None, ge=0)
    storage_location: Optional[str] = None
    storage_condition: Optional[StorageCondition] = None
    status: Optional[InventoryStatus] = None
    supplier_id: Optional[str] = None
    supplier_name: Optional[str] = None
    unit_cost: Optional[float] = Field(None, gt=0)
    last_ordered_date: Optional[datetime] = None
    last_received_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    lot_number: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    total_received: Optional[float] = Field(None, ge=0)
    total_issued: Optional[float] = Field(None, ge=0)
    total_adjusted: Optional[float] = None
    last_count_date: Optional[datetime] = None
    last_count_quantity: Optional[float] = Field(None, ge=0)

    @validator('maximum_stock_level')
    def validate_maximum_stock_level(cls, v, values):
        if v and 'minimum_stock_level' in values and values['minimum_stock_level'] is not None:
            if v < values['minimum_stock_level']:
                raise ValueError("Maximum stock level must be greater than minimum stock level")
        return v

    @validator('reorder_point')
    def validate_reorder_point(cls, v, values):
        if v:
            if 'minimum_stock_level' in values and values['minimum_stock_level'] is not None:
                if v < values['minimum_stock_level']:
                    raise ValueError("Reorder point must be greater than or equal to minimum stock level")
            if 'maximum_stock_level' in values and values['maximum_stock_level'] is not None:
                if v > values['maximum_stock_level']:
                    raise ValueError("Reorder point must be less than or equal to maximum stock level")
        return v

# Schema for inventory item response
class InventoryManagementResponse(InventoryManagementBase):
    id: int = Field(..., description="Database ID of the inventory item")
    created_at: datetime = Field(..., description="Timestamp when the inventory item was created")
    updated_at: datetime = Field(..., description="Timestamp when the inventory item was last updated")

    class Config:
        orm_mode = True

# Schema for inventory item list response
class InventoryManagementList(BaseModel):
    items: List[InventoryManagementResponse]
    total: int
    page: int
    size: int
    pages: int 