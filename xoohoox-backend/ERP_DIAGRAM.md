# Xoohoox ERP System Diagram

## Process Flow Diagram
```mermaid
graph TD
    subgraph "Raw Material Management"
        RM1[Fruit Procurement] --> RM2[Quality Inspection]
        RM2 --> RM3[Storage Management]
        RM3 --> RM4[Inventory Tracking]
    end

    subgraph "Production Process"
        PP1[Raw Input Preparation] --> PP2[Juicing Process]
        PP2 --> PP3[Chemistry Correction]
        PP3 --> PP4[Heat Activation]
        PP4 --> PP5[Fermentation]
        PP5 --> PP6[Quality Control]
        PP6 --> PP7[Branch Decision]
    end

    subgraph "Branch A: Distillation"
        BA1[First Distillation] --> BA2[Quality Testing]
        BA2 --> BA3[Second Distillation]
        BA3 --> BA4[Final Quality Control]
        BA4 --> BA5[Packaging]
    end

    subgraph "Branch B: Vinegar"
        BB1[Vinegar Fermentation] --> BB2[Acidity Control]
        BB2 --> BB3[Quality Testing]
        BB3 --> BB4[Packaging]
    end

    subgraph "Quality Management"
        QM1[In-Process Testing] --> QM2[Quality Metrics]
        QM2 --> QM3[Corrective Actions]
        QM3 --> QM4[Documentation]
    end

    subgraph "Equipment Management"
        EM1[Maintenance Schedule] --> EM2[Equipment Status]
        EM2 --> EM3[Maintenance Records]
        EM3 --> EM4[Performance Tracking]
    end

    subgraph "Reporting & Analytics"
        RA1[Production Reports] --> RA2[Quality Reports]
        RA2 --> RA3[Equipment Reports]
        RA3 --> RA4[Performance Analytics]
    end

    PP7 -->|ABV 8-13%| BB1
    PP7 -->|ABV >13%| BA1

    style Raw_Material_Management fill:#f9f,stroke:#333,stroke-width:2px
    style Production_Process fill:#bbf,stroke:#333,stroke-width:2px
    style Branch_A fill:#bfb,stroke:#333,stroke-width:2px
    style Branch_B fill:#fbb,stroke:#333,stroke-width:2px
    style Quality_Management fill:#ff9,stroke:#333,stroke-width:2px
    style Equipment_Management fill:#9ff,stroke:#333,stroke-width:2px
    style Reporting_Analytics fill:#f9f,stroke:#333,stroke-width:2px
```

## Swimlane Diagram
```mermaid
graph LR
    subgraph "Procurement Department"
        P1[Fruit Procurement]
        P2[Quality Inspection]
        P3[Inventory Management]
    end

    subgraph "Production Department"
        PD1[Raw Input Prep]
        PD2[Juicing]
        PD3[Chemistry]
        PD4[Heat Activation]
        PD5[Fermentation]
    end

    subgraph "Quality Department"
        Q1[In-Process Testing]
        Q2[Quality Control]
        Q3[Final Testing]
    end

    subgraph "Processing Department"
        PR1[Distillation]
        PR2[Vinegar Production]
    end

    subgraph "Maintenance Department"
        M1[Equipment Monitoring]
        M2[Maintenance Scheduling]
        M3[Performance Tracking]
    end

    subgraph "Administration"
        A1[Reporting]
        A2[Analytics]
        A3[Documentation]
    end

    %% Process Flow
    P1 --> P2 --> P3
    P3 --> PD1
    PD1 --> PD2 --> PD3 --> PD4 --> PD5
    PD5 --> Q1
    Q1 --> Q2
    Q2 -->|ABV >13%| PR1
    Q2 -->|ABV 8-13%| PR2
    PR1 --> Q3
    PR2 --> Q3

    %% Support Processes
    M1 --> M2 --> M3
    M1 -.-> PD1
    M1 -.-> PD2
    M1 -.-> PD3
    M1 -.-> PD4
    M1 -.-> PD5
    M1 -.-> PR1
    M1 -.-> PR2

    Q1 -.-> A1
    Q2 -.-> A1
    Q3 -.-> A1
    M3 -.-> A1
    A1 --> A2 --> A3

    style Procurement_Department fill:#f9f,stroke:#333,stroke-width:2px
    style Production_Department fill:#bbf,stroke:#333,stroke-width:2px
    style Quality_Department fill:#ff9,stroke:#333,stroke-width:2px
    style Processing_Department fill:#bfb,stroke:#333,stroke-width:2px
    style Maintenance_Department fill:#9ff,stroke:#333,stroke-width:2px
    style Administration fill:#f9f,stroke:#333,stroke-width:2px
```

## Departmental View Explanation

1. **Procurement Department** (Pink)
   - Handles all raw material acquisition
   - Manages initial quality checks
   - Controls inventory levels

2. **Production Department** (Blue)
   - Manages the core production process
   - Handles all transformation stages
   - Coordinates with quality department

3. **Quality Department** (Yellow)
   - Conducts testing at various stages
   - Makes critical process decisions
   - Ensures product standards

4. **Processing Department** (Green)
   - Handles final product processing
   - Manages both distillation and vinegar paths
   - Works closely with quality control

5. **Maintenance Department** (Cyan)
   - Monitors equipment health
   - Schedules maintenance
   - Tracks performance metrics

6. **Administration** (Pink)
   - Generates reports
   - Performs analytics
   - Maintains documentation

## Key Interactions
- Dotted lines (.-.) show support processes
- Solid lines (--) show main process flow
- Quality department makes the critical ABV decision
- Maintenance supports all production processes
- Administration receives data from all departments 

## Traditional RDBMS Diagram
```mermaid
classDiagram
    class FRUITS {
        +int fruit_id PK
        +varchar fruit_type
        +decimal quantity
        +date received_date
        +varchar supplier
        +varchar quality_grade
    }

    class BATCHES {
        +int batch_id PK
        +int fruit_id FK
        +date creation_date
        +varchar status
        +decimal initial_volume
        +varchar process_type
    }

    class JUICE_PREPARATION {
        +int prep_id PK
        +int batch_id FK
        +decimal input_volume
        +decimal output_volume
        +decimal yield_percentage
        +json process_parameters
        +timestamp completion_time
    }

    class CHEMISTRY_ANALYSIS {
        +int analysis_id PK
        +int batch_id FK
        +decimal ph_value
        +decimal specific_gravity
        +decimal sugar_content
        +json adjustments
        +timestamp analysis_time
    }

    class FERMENTATION {
        +int fermentation_id PK
        +int batch_id FK
        +decimal temperature
        +decimal alcohol_content
        +timestamp start_time
        +timestamp end_time
        +json environmental_conditions
    }

    class DISTILLATION {
        +int distillation_id PK
        +int batch_id FK
        +int distillation_stage
        +decimal alcohol_content
        +decimal volume
        +timestamp completion_time
        +json quality_metrics
    }

    class VINEGAR_PRODUCTION {
        +int vinegar_id PK
        +int batch_id FK
        +decimal acidity
        +decimal volume
        +timestamp start_time
        +timestamp end_time
        +json process_parameters
    }

    class QUALITY_CONTROL {
        +int qc_id PK
        +int batch_id FK
        +int user_id FK
        +varchar test_type
        +json test_results
        +boolean passed
        +timestamp test_time
    }

    class EQUIPMENT {
        +int equipment_id PK
        +varchar equipment_name
        +varchar equipment_type
        +varchar status
        +date last_maintenance
        +date next_maintenance
    }

    class MAINTENANCE_RECORDS {
        +int maintenance_id PK
        +int equipment_id FK
        +int user_id FK
        +date maintenance_date
        +varchar maintenance_type
        +varchar description
        +decimal cost
    }

    class PRODUCTION_RUNS {
        +int run_id PK
        +int equipment_id FK
        +int batch_id FK
        +timestamp start_time
        +timestamp end_time
        +json performance_metrics
    }

    class USERS {
        +int user_id PK
        +varchar username
        +varchar role
        +varchar department
        +boolean is_active
    }

    FRUITS "1" -- "many" BATCHES : "used_in"
    BATCHES "1" -- "many" JUICE_PREPARATION : "has"
    BATCHES "1" -- "many" CHEMISTRY_ANALYSIS : "has"
    BATCHES "1" -- "many" FERMENTATION : "has"
    BATCHES "1" -- "many" DISTILLATION : "has"
    BATCHES "1" -- "many" VINEGAR_PRODUCTION : "has"
    BATCHES "1" -- "many" QUALITY_CONTROL : "has"
    EQUIPMENT "1" -- "many" MAINTENANCE_RECORDS : "requires"
    EQUIPMENT "1" -- "many" PRODUCTION_RUNS : "used_in"
    USERS "1" -- "many" QUALITY_CONTROL : "performs"
    USERS "1" -- "many" MAINTENANCE_RECORDS : "performs"
```

## Table Relationships Explanation

1. **Core Production Tables**
   - `FRUITS` to `BATCHES`: One-to-many (one fruit type can be used in many batches)
   - `BATCHES` to process tables: One-to-many (one batch can have multiple process steps)

2. **Process Tables**
   - `JUICE_PREPARATION`: Tracks initial processing
   - `CHEMISTRY_ANALYSIS`: Records chemical properties
   - `FERMENTATION`: Tracks fermentation process
   - `DISTILLATION`: Records distillation stages
   - `VINEGAR_PRODUCTION`: Tracks vinegar making process

3. **Quality and Equipment**
   - `QUALITY_CONTROL`: Links batches to users and test results
   - `EQUIPMENT`: Tracks all production equipment
   - `MAINTENANCE_RECORDS`: Links equipment to maintenance history
   - `PRODUCTION_RUNS`: Tracks equipment usage

4. **User Management**
   - `USERS`: Manages system users and their roles
   - Links to quality control and maintenance records

## Key Features
- Primary Keys (PK) for all tables
- Foreign Keys (FK) for relationships
- Timestamps for process tracking
- JSON fields for flexible data storage
- Decimal precision for measurements
- Status tracking for batches and equipment 