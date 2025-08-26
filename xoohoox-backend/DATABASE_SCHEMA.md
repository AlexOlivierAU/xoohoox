# Xoohoox Fermentation & Distillation Management System - Database Schema

## Tables and Relationships

```
+-------------------+       +-------------------+       +-------------------+
|   BatchTracking   |       |  JuicingInputLog  |       |  QualityControl   |
+-------------------+       +-------------------+       +-------------------+
| id                |       | id                |       | id                |
| batch_id          |<------| batch_id          |       | test_id           |
| arrival_date      |       | log_id            |       | batch_id          |<----+
| fruit_type        |       | timestamp         |       | test_type         |     |
| supplier_name     |       | operator_id       |       | test_date         |     |
| supplier_batch_id |       | equipment_id      |       | test_name         |     |
| quantity_kg       |       | input_quantity_kg |       | test_method       |     |
| quality_grade     |       | output_quantity_kg|       | test_parameters   |     |
| storage_location  |       | process_status    |       | expected_range_min|     |
| storage_conditions|       | notes             |       | expected_range_max|     |
| initial_notes     |       +-------------------+       | actual_value      |     |
| status            |                                   | unit_of_measure   |     |
| processing_start_date|                               | result            |     |
| processing_end_date  |                               | tester_id         |     |
| final_product_type  |                               | equipment_used    |     |
| final_product_quantity|                             | temperature_c     |     |
| quality_issues      |                               | humidity_percent  |     |
+-------------------+                                 | notes             |     |
        |                                             | corrective_actions|     |
        |                                             | retest_required   |     |
        |                                             +-------------------+     |
        |                                                                       |
        |                                                                       |
        v                                                                       |
+-------------------+       +-------------------+       +-------------------+
|EquipmentMaintenance|       |InventoryManagement|       |     Users         |
+-------------------+       +-------------------+       +-------------------+
| id                |       | id                |       | id                |
| maintenance_id    |       | item_id           |       | username          |
| equipment_id      |       | item_name         |       | email             |
| equipment_type    |       | item_type         |       | hashed_password   |
| equipment_name    |       | description       |       | full_name         |
| manufacturer      |       | sku               |       | is_active         |
| model_number      |       | barcode           |       | is_superuser      |
| serial_number     |       | unit_of_measure   |       | created_at        |
| installation_date |       | quantity_in_stock |       | updated_at        |
| maintenance_type  |       | minimum_stock_level|      +-------------------+
| maintenance_status|       | reorder_point     |
| scheduled_date    |       | maximum_stock_level|
| actual_date       |       | storage_location  |
| technician_id     |       | storage_condition |
| cost              |       | status            |
| parts_replaced    |       | supplier_id       |
| work_performed    |       | supplier_name     |
| results           |       | unit_cost         |
| next_maintenance_date|    | last_ordered_date |
| requires_shutdown |       | last_received_date|
| shutdown_duration_hours|  | expiry_date       |
| notes             |       | lot_number        |
| is_critical       |       | is_active         |
+-------------------+       | notes             |
                            | total_received    |
                            | total_issued      |
                            | total_adjusted    |
                            | last_count_date   |
                            | last_count_quantity|
                            +-------------------+
```

## Relationships

1. **BatchTracking** has many **JuicingInputLog** entries (one-to-many)
   - A batch can have multiple juicing logs
   - Each juicing log belongs to one batch

2. **BatchTracking** has many **QualityControl** tests (one-to-many)
   - A batch can have multiple quality tests
   - Each quality test belongs to one batch

3. **EquipmentMaintenance** is independent
   - No direct relationships with other tables

4. **InventoryManagement** is independent
   - No direct relationships with other tables

## Key Fields

1. **BatchTracking**
   - `batch_id`: Unique identifier for each batch
   - `status`: Current status of the batch (RECEIVED, IN_STORAGE, IN_PROCESSING, COMPLETED, REJECTED)

2. **JuicingInputLog**
   - `log_id`: Unique identifier for each log entry
   - `batch_id`: Reference to the batch
   - `process_status`: Current status of the juicing process

3. **QualityControl**
   - `test_id`: Unique identifier for each test
   - `batch_id`: Reference to the batch
   - `result`: Result of the test (PASS, FAIL, PENDING, INCONCLUSIVE)

4. **EquipmentMaintenance**
   - `maintenance_id`: Unique identifier for each maintenance record
   - `equipment_id`: Unique identifier for the equipment
   - `maintenance_status`: Current status of the maintenance

5. **InventoryManagement**
   - `item_id`: Unique identifier for each inventory item
   - `status`: Current status of the inventory item
   - `quantity_in_stock`: Current quantity in stock

## Enums

1. **BatchTracking**
   - `FruitType`: ORANGE, APPLE, GRAPE, PINEAPPLE, MANGO, OTHER
   - `QualityGrade`: A, B, C, REJECTED
   - `FinalProductType`: JUICE, CONCENTRATE, PUREE, DISTILLATE, VINEGAR, OTHER
   - `BatchStatus`: RECEIVED, IN_STORAGE, IN_PROCESSING, COMPLETED, REJECTED

2. **JuicingInputLog**
   - `ProcessStatus`: STARTED, IN_PROGRESS, COMPLETED, PAUSED, FAILED

3. **QualityControl**
   - `TestType`: MICROBIAL, CHEMICAL, PHYSICAL, SENSORY, COMPOUND, OTHER
   - `TestResult`: PASS, FAIL, PENDING, INCONCLUSIVE

4. **EquipmentMaintenance**
   - `MaintenanceType`: PREVENTIVE, CORRECTIVE, CALIBRATION, INSPECTION, CLEANING
   - `MaintenanceStatus`: SCHEDULED, IN_PROGRESS, COMPLETED, DELAYED, CANCELLED
   - `EquipmentType`: JUICER, FERMENTER, DISTILLER, FILTER, PUMP, TANK, SENSOR, OTHER

5. **InventoryManagement**
   - `ItemType`: RAW_MATERIAL, PACKAGING, FINISHED_PRODUCT, CLEANING_SUPPLY, SPARE_PART, OTHER
   - `StorageCondition`: AMBIENT, REFRIGERATED, FROZEN, CONTROLLED
   - `InventoryStatus`: IN_STOCK, LOW_STOCK, OUT_OF_STOCK, EXPIRED, RESERVED, DISCONTINUED 