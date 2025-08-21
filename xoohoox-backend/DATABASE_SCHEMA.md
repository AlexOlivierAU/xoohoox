# Xoohoox Fermentation & Distillation Management System - Complete Database Schema

## 🎯 **Current Status: COMPLETE** 
- **Database**: PostgreSQL 14
- **Tables**: 41
- **Total Fields**: 553
- **Enum Types**: 14
- **Status**: ✅ Production Ready

## 📊 **Database Overview**

### **Core Production Tables**
```
+-------------------+       +-------------------+       +-------------------+
|   BatchTracking   |       |  BatchDispatches  |       |  FermentationTrials |
+-------------------+       +-------------------+       +-------------------+
| id (PK)           |       | id (PK)           |       | id (PK)           |
| batch_id (UK)     |       | batch_id (UK)     |       | trial_id (UK)     |
| name              |       | grower_id         |       | batch_id (FK)     |
| fruit_type (ENUM) |       | produce_type      |       | yeast_strain      |
| process_type      |       | varietal          |       | juice_variant     |
| grower_id         |       | dispatch_date     |       | initial_volume    |
| status            |       | quantity_kg       |       | sg                |
| stage             |       +-------------------+       | ph                |
| progress          |                                   | brix              |
| start_date        |                                   | current_abv       |
| end_date          |                                   | path_taken        |
| quality_checks    |                                   | status            |
| maintenance_records|                                  | daily_readings    |
| environmental_impact|                                 | upscale_history   |
| processing_start_date|                               | compound_results  |
| processing_end_date|                                 +-------------------+
| final_product_quantity|                                       |
| production_date   |                                           |
| recipe_id         |                                           |
| ingredients       |                                           |
| juice_type (ENUM) |                                           |
| target_quantity   |                                           |
| actual_quantity   |                                           |
| completion_date   |                                           |
| quality_grade     |                                           |
| actual_ingredients|                                           |
| temperature       |                                           |
| ph_level          |                                           |
| brix              |                                           |
| processing_time   |                                           |
| issues            |                                           |
| corrective_actions|                                           |
| created_by        |                                           |
| updated_by        |                                           |
| created_at        |                                           |
| updated_at        |                                           |
+-------------------+                                           |
        |                                                       |
        |                                                       |
        v                                                       |
+-------------------+       +-------------------+               |
|TransformationStages|       |  UpscaleRuns     |               |
+-------------------+       +-------------------+               |
| id (PK)           |       | id (PK)           |               |
| batch_id          |       | upscale_id (UK)   |               |
| stage_number      |       | trial_id (FK)     |               |
| stage_name        |       | stage (ENUM)      |               |
| stage_type (ENUM) |       | volume            |               |
| status (ENUM)     |       | yield_amount      |               |
| total_trials      |       | abv_result        |               |
| trials_to_proceed |       | compound_summary  |               |
| parent_stage_id   |       | status (ENUM)     |               |
| upscale_factor    |       | timestamp         |               |
| target_volume     |       +-------------------+               |
| planned_duration_days|                                       |
| actual_duration_days|                                        |
| branching_rule    |                                           |
| created_at        |                                           |
| updated_at        |                                           |
+-------------------+                                           |
        |                                                       |
        |                                                       |
        v                                                       |
+-------------------+       +-------------------+               |
|  JuicingResults   |       |  QualityControl   |               |
+-------------------+       +-------------------+               |
| id (PK)           |       | id (PK)           |               |
| stage_id (FK)     |       | test_id (UK)      |               |
| juice_processing_type|    | batch_id (FK)     |               |
| is_raw_juice_ferment|     | test_type         |               |
| input_weight      |       | test_date         |               |
| fruit_condition   |       | test_name         |               |
| juice_volume      |       | test_method       |               |
| juice_yield       |       | test_parameters   |               |
| juice_yield_per_gram|     | expected_range_min|               |
| brix              |       | expected_range_max|               |
| ph                |       | actual_value      |               |
| temperature       |       | unit_of_measure   |               |
| press_pressure    |       | result            |               |
| press_time        |       | tester_id         |               |
| maceration_time   |       | equipment_used    |               |
| extraction_method |       | temperature_c     |               |
| notes             |       | humidity_percent  |               |
| created_at        |       | notes             |               |
| updated_at        |       | corrective_actions|               |
+-------------------+       | retest_required   |               |
                            | created_at        |               |
                            | updated_at        |               |
                            +-------------------+               |
```

### **Process & Results Tables**
```
+-------------------+       +-------------------+       +-------------------+
|ChemistryResults   |       |HeatActivationResults|     |FermentationResults|
+-------------------+       +-------------------+       +-------------------+
| id (PK)           |       | id (PK)           |       | id (PK)           |
| stage_id (FK)     |       | stage_id (FK)     |       | stage_id (FK)     |
| ph_initial        |       | heating_method    |       | initial_gravity   |
| ph_adjusted       |       | target_temperature|       | final_gravity     |
| titratable_acidity|       | actual_temperature|       | abv               |
| sulfite_addition  |       | heating_duration  |       | temperature       |
| nutrient_addition |       | cooling_method    |       | ph                |
| enzyme_addition   |       | final_temperature |       | notes             |
| clarification_agent|      | post_heat_ph      |       | created_at        |
| clarification_amount|     | clarity_improvement|      | updated_at        |
| notes             |       | notes             |       +-------------------+
| created_at        |       | created_at        |
| updated_at        |       | updated_at        |
+-------------------+       +-------------------+
```

### **Equipment & Maintenance Tables**
```
+-------------------+       +-------------------+       +-------------------+
|Equipment          |       |EquipmentMaintenance|      |MaintenanceLog     |
+-------------------+       +-------------------+       +-------------------+
| id (PK)           |       | id (PK)           |       | id (PK)           |
| equipment_id (UK) |       | maintenance_id(UK)|       | equipment_id      |
| name              |       | equipment_id      |       | maintenance_date  |
| type              |       | equipment_type    |       | maintenance_type  |
| manufacturer      |       | equipment_name    |       | performed_by      |
| model             |       | manufacturer      |       | description       |
| serial_number     |       | model_number      |       | cost              |
| purchase_date     |       | serial_number     |       | next_maintenance_date|
| warranty_expiry   |       | installation_date |       | notes             |
| status            |       | maintenance_type  |       | created_at        |
| location          |       | maintenance_status|       | updated_at        |
| notes             |       | scheduled_date    |       +-------------------+
| created_at        |       | actual_date       |
| updated_at        |       | technician_id     |
+-------------------+       | cost              |
                            | parts_replaced    |
                            | work_performed    |
                            | results           |
                            | next_maintenance_date|
                            | requires_shutdown |
                            | shutdown_duration_hours|
                            | notes             |
                            | is_critical       |
                            | created_at        |
                            | updated_at        |
                            +-------------------+
```

### **Inventory & Management Tables**
```
+-------------------+       +-------------------+       +-------------------+
|InventoryManagement|       |Users              |       |Farms              |
+-------------------+       +-------------------+       +-------------------+
| id (PK)           |       | id (PK)           |       | id (PK)           |
| item_id (UK)      |       | email (UK)        |       | name              |
| item_name         |       | username (UK)     |       | location          |
| item_type (ENUM)  |       | hashed_password   |       | contact_info      |
| description       |       | full_name         |       | notes             |
| sku (UK)          |       | is_active         |       | created_at        |
| barcode (UK)      |       | is_superuser      |       | updated_at        |
| unit_of_measure   |       | created_at        |       +-------------------+
| quantity_in_stock |       | updated_at        |
| minimum_stock_level|      +-------------------+
| reorder_point     |
| maximum_stock_level|
| storage_location  |
| storage_condition (ENUM)|
| status (ENUM)     |
| supplier_id       |
| supplier_name     |
| unit_cost         |
| last_ordered_date |
| last_received_date|
| expiry_date       |
| lot_number        |
| is_active         |
| notes             |
| total_received    |
| total_issued      |
| total_adjusted    |
| last_count_date   |
| last_count_quantity|
| created_at        |
| updated_at        |
+-------------------+
```

## 🔗 **Key Relationships**

### **Primary Relationships**
1. **BatchTracking** → **JuicingInputLog** (one-to-many)
2. **BatchTracking** → **QualityControl** (one-to-many)
3. **BatchTracking** → **TransformationStages** (one-to-many)
4. **FermentationTrials** → **UpscaleRuns** (one-to-many)
5. **TransformationStages** → **JuicingResults** (one-to-many)
6. **TransformationStages** → **ChemistryResults** (one-to-many)
7. **TransformationStages** → **HeatActivationResults** (one-to-many)
8. **TransformationStages** → **FermentationResults** (one-to-many)
9. **TransformationStages** → **VinegarResults** (one-to-many)
10. **TransformationStages** → **DistillationResults** (one-to-many)
11. **TransformationStages** → **Stage2Results** (one-to-many)
12. **TransformationStages** → **FruitPerformance** (one-to-many)

### **Equipment Relationships**
1. **Equipment** → **EquipmentMaintenance** (one-to-many)
2. **Equipment** → **MaintenanceLog** (one-to-many)

## 📋 **Complete Table List (41 Tables)**

### **Core Production (8 tables)**
- `batch_tracking` (36 fields) - Main batch management
- `batch_dispatches` (7 fields) - Batch dispatch information
- `batch` (6 fields) - Basic batch records
- `fermentation_trials` (17 fields) - Fermentation experiments
- `upscale_runs` (10 fields) - Production scaling
- `transformation_stages` (16 fields) - Production stages
- `juicing_input_log` (12 fields) - Input logging
- `juicing_input_log_detailed` (14 fields) - Detailed input logging

### **Process Results (12 tables)**
- `juicing_results` (19 fields) - Juicing process results
- `juicing_results_detailed` (10 fields) - Detailed juicing results
- `chemistry_results` (13 fields) - Chemistry analysis
- `heat_activation_results` (13 fields) - Heat treatment results
- `fermentation_results` (10 fields) - Fermentation outcomes
- `fermentation_results_detailed` (14 fields) - Detailed fermentation results
- `vinegar_results` (15 fields) - Vinegar production
- `vinegar_kinetics` (15 fields) - Vinegar kinetics
- `distillation_results` (14 fields) - Distillation outcomes
- `distillation_results_detailed` (18 fields) - Detailed distillation results
- `stage2_results` (15 fields) - Secondary processing
- `fruit_performance` (15 fields) - Fruit quality tracking

### **Quality & Evaluation (6 tables)**
- `quality_control` (22 fields) - Quality testing
- `produce_prelim_eval` (17 fields) - Produce evaluation
- `product_evaluation` (11 fields) - Product evaluation
- `sensory_feedback` (13 fields) - Sensory feedback
- `evaluations` (9 fields) - General evaluations
- `failure_reports` (11 fields) - Process failures

### **Equipment & Maintenance (3 tables)**
- `equipment` (14 fields) - Equipment records
- `equipment_maintenance` (25 fields) - Maintenance tracking
- `maintenance_log` (11 fields) - Maintenance logs

### **Inventory & Management (3 tables)**
- `inventory_management` (31 fields) - Stock tracking
- `users` (9 fields) - User management
- `farms` (7 fields) - Farm information

### **Planning & Kinetics (6 tables)**
- `fermentation_plan` (14 fields) - Fermentation planning
- `fermentation_kinetics` (10 fields) - Fermentation kinetics
- `liquefaction_method` (10 fields) - Liquefaction methods
- `liquefaction_plan` (12 fields) - Liquefaction planning
- `liquefaction_runs` (12 fields) - Liquefaction runs
- `yeast_strains` (8 fields) - Yeast data

### **Logs & Tracking (3 tables)**
- `fermentation_logs` (9 fields) - Fermentation tracking
- `juicing_logs` (8 fields) - Juicing logs
- `alembic_version` (1 field) - Migration tracking

## 🎯 **Enum Types (14 Types)**

1. **fruittype** - APPLE, PEAR, GRAPE, MIXED, OTHER
2. **batchstatus** - PLANNED, IN_PROGRESS, COMPLETED, CANCELLED, FAILED
3. **qualitygrade** - A, B, C, REJECT
4. **juicetype** - APPLE, PEAR, GRAPE, MIXED
5. **processstatus** - PLANNED, IN_PROGRESS, COMPLETED, FAILED
6. **transformationtype** - CHEMISTRY_PREP, HEAT_ACTIVATION, INITIAL_FERMENTATION, UPSCALE_FERMENTATION, VINEGAR_PROCESSING, DISTILLATION, STAGE_2_PROCESSING, DRYING, COMPOSTING, MARKET_SALE, OTHER
7. **juiceprocessingtype** - JP1, JP2, JP3, JP4, JP5
8. **pathtaken** - vinegar, distillation, archived
9. **juicevariant** - JP1, JP2, JP3, JP4, JP5
10. **upscalestage** - Test 4, Test 5, Test 6
11. **upscalestatus** - pending, complete, failed
12. **itemtype** - RAW_MATERIAL, PACKAGING, CHEMICAL, EQUIPMENT, CONSUMABLE
13. **storagecondition** - AMBIENT, REFRIGERATED, FROZEN, CONTROLLED
14. **inventorystatus** - ACTIVE, INACTIVE, DISCONTINUED

## 🚀 **Database Statistics**

- **Total Tables**: 41
- **Total Fields**: 553
- **Enum Types**: 14
- **Indexes**: 28 (for performance)
- **Foreign Keys**: 15 (for data integrity)
- **Sequences**: 41 (for auto-increment)

## ✅ **Verification Commands**

```bash
# Check total counts
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "SELECT 'Tables: ' || COUNT(*)::text FROM information_schema.tables WHERE table_schema = 'public';"
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "SELECT 'Fields: ' || COUNT(*)::text FROM information_schema.columns WHERE table_schema = 'public';"

# List all tables
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "\dt"

# View table structure
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "\d table_name"

# List enum types
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "\dT+"
```

## 🎉 **Status: PRODUCTION READY**

The database schema is now complete and ready for the XooHooX juice production management system. All 553 fields across 41 tables are properly structured with relationships, indexes, and data integrity constraints. 