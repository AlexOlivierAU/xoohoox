# API Endpoints Documentation

This directory contains the API endpoints for the Xoohoox backend application. Each file represents a specific module of functionality.

## Available Endpoints

### Authentication
- `login.py`: Authentication endpoints for user login and token management

### Batch Tracking
- `batch_tracking.py`: Endpoints for managing juice production batches

### Quality Control
- `quality_control.py`: Endpoints for managing quality control tests and results

### Equipment Maintenance
- `equipment_maintenance.py`: Endpoints for managing equipment maintenance

## Equipment Maintenance Module

The equipment maintenance module provides a comprehensive set of endpoints for managing equipment maintenance in the juice production facility.

### Base Endpoints

- `POST /`: Create a new equipment maintenance record
- `GET /`: List maintenance records with optional filtering
- `GET /{maintenance_id}`: Get a specific maintenance record
- `PUT /{maintenance_id}`: Update a maintenance record
- `DELETE /{maintenance_id}`: Delete a maintenance record

### Specialized Endpoints

- `GET /equipment/{equipment_id}`: Get all maintenance records for a specific equipment
- `POST /{maintenance_id}/start`: Start a scheduled maintenance
- `POST /{maintenance_id}/complete`: Complete a maintenance that is in progress
- `POST /{maintenance_id}/delay`: Delay a scheduled maintenance
- `POST /{maintenance_id}/cancel`: Cancel a scheduled maintenance

### Maintenance Lifecycle

The equipment maintenance module supports a complete maintenance lifecycle:

1. **Scheduling**: Create a new maintenance record with status `SCHEDULED`
2. **Starting**: Change status to `IN_PROGRESS` when maintenance begins
3. **Completing**: Change status to `COMPLETED` when maintenance is finished
4. **Delaying**: Change status to `DELAYED` if maintenance needs to be rescheduled
5. **Cancelling**: Change status to `CANCELLED` if maintenance is no longer needed

### Filtering Options

The list endpoint supports filtering by:
- `equipment_id`: Filter by specific equipment
- `maintenance_type`: Filter by type (PREVENTIVE, CORRECTIVE, etc.)
- `maintenance_status`: Filter by status (SCHEDULED, IN_PROGRESS, etc.)
- `equipment_type`: Filter by equipment type (JUICER, PASTEURIZER, etc.)
- `is_critical`: Filter by criticality

### Pagination

All list endpoints support pagination with:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 10, max: 100)

### Authentication

All endpoints require authentication via JWT token. The token must be provided in the Authorization header. 