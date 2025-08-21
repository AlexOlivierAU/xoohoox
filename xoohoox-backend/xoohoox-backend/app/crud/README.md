# CRUD Operations Documentation

This directory contains the CRUD (Create, Read, Update, Delete) operations for the Xoohoox backend application. Each file represents a specific module of functionality.

## Available CRUD Modules

### Authentication
- `user.py`: User management operations

### Batch Tracking
- `batch_tracking.py`: Operations for managing juice production batches

### Quality Control
- `quality_control.py`: Operations for managing quality control tests and results

### Equipment Maintenance
- `equipment_maintenance.py`: Operations for managing equipment maintenance

## Equipment Maintenance Module

The equipment maintenance module provides a comprehensive set of CRUD operations for managing equipment maintenance in the juice production facility.

### Base Operations

- `create`: Create a new equipment maintenance record
- `get`: Get a maintenance record by ID
- `get_multi`: Get multiple maintenance records with filtering
- `update`: Update a maintenance record
- `remove`: Delete a maintenance record

### Specialized Operations

- `get_by_maintenance_id`: Get a maintenance record by maintenance ID
- `get_by_equipment_id`: Get all maintenance records for a specific equipment
- `count`: Count maintenance records with filtering
- `start_maintenance`: Start a scheduled maintenance
- `complete_maintenance`: Complete a maintenance that is in progress
- `delay_maintenance`: Delay a scheduled maintenance
- `cancel_maintenance`: Cancel a scheduled maintenance

### Filtering Options

The `get_multi` and `count` operations support filtering by:
- `equipment_id`: Filter by specific equipment
- `maintenance_type`: Filter by type (PREVENTIVE, CORRECTIVE, etc.)
- `maintenance_status`: Filter by status (SCHEDULED, IN_PROGRESS, etc.)
- `equipment_type`: Filter by equipment type (JUICER, PASTEURIZER, etc.)
- `is_critical`: Filter by criticality

### Pagination

The `get_multi` operation supports pagination with:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

### Maintenance Lifecycle

The equipment maintenance module supports a complete maintenance lifecycle:

1. **Scheduling**: Create a new maintenance record with status `SCHEDULED`
2. **Starting**: Change status to `IN_PROGRESS` when maintenance begins
3. **Completing**: Change status to `COMPLETED` when maintenance is finished
4. **Delaying**: Change status to `DELAYED` if maintenance needs to be rescheduled
5. **Cancelling**: Change status to `CANCELLED` if maintenance is no longer needed

### Implementation Details

The equipment maintenance module extends the base CRUD class and adds specialized methods for maintenance management. It includes validation logic to ensure proper state transitions and data integrity. 