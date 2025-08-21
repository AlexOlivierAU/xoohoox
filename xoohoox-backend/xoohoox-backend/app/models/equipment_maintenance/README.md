# Equipment Maintenance Module

The Equipment Maintenance module is a core component of the Xoohoox juice production management system. It provides functionality for tracking and managing equipment maintenance in the production facility.

## Overview

This module allows users to:
- Schedule maintenance for equipment
- Track maintenance activities
- Monitor equipment status
- Manage the maintenance lifecycle
- Generate maintenance reports

## Data Model

The Equipment Maintenance model includes the following key fields:

### Identifiers
- `id`: Primary key
- `maintenance_id`: Unique identifier for the maintenance record
- `equipment_id`: Unique identifier for the equipment

### Equipment Information
- `equipment_type`: Type of equipment (JUICER, PASTEURIZER, etc.)
- `equipment_name`: Name of the equipment
- `manufacturer`: Manufacturer of the equipment
- `model_number`: Model number of the equipment
- `serial_number`: Serial number of the equipment
- `installation_date`: Date when the equipment was installed

### Maintenance Information
- `maintenance_type`: Type of maintenance (PREVENTIVE, CORRECTIVE, etc.)
- `maintenance_status`: Current status of the maintenance
- `scheduled_date`: Date when maintenance is scheduled
- `actual_date`: Date when maintenance was actually performed
- `technician_id`: ID of the technician performing the maintenance
- `cost`: Cost of the maintenance
- `parts_replaced`: Parts that were replaced
- `work_performed`: Description of work performed
- `results`: Results of the maintenance
- `next_maintenance_date`: Date of next scheduled maintenance

### Operational Information
- `requires_shutdown`: Whether the maintenance requires equipment shutdown
- `shutdown_duration_hours`: Duration of shutdown in hours
- `notes`: Additional notes about the maintenance
- `is_critical`: Whether the maintenance is critical

### Audit Information
- `created_at`: Timestamp when the record was created
- `updated_at`: Timestamp when the record was last updated
- `created_by`: User who created the record
- `updated_by`: User who last updated the record

## Enums

### MaintenanceType
- `PREVENTIVE`: Regular maintenance to prevent issues
- `CORRECTIVE`: Maintenance to fix existing issues
- `CALIBRATION`: Calibration of equipment
- `INSPECTION`: Inspection of equipment
- `CLEANING`: Cleaning of equipment

### MaintenanceStatus
- `SCHEDULED`: Maintenance is scheduled
- `IN_PROGRESS`: Maintenance is in progress
- `COMPLETED`: Maintenance is completed
- `DELAYED`: Maintenance is delayed
- `CANCELLED`: Maintenance is cancelled

### EquipmentType
- `JUICER`: Juicing equipment
- `PASTEURIZER`: Pasteurization equipment
- `FILTER`: Filtration equipment
- `PUMP`: Pumping equipment
- `TANK`: Storage tank
- `SENSOR`: Monitoring sensor
- `OTHER`: Other equipment

## Relationships

The Equipment Maintenance model is designed to be independent and does not have direct relationships with other models. This allows for flexible maintenance tracking without tight coupling to other parts of the system.

## Usage

The Equipment Maintenance module is used by:
- Maintenance technicians to record and track maintenance activities
- Production managers to schedule maintenance and monitor equipment status
- Quality control personnel to ensure equipment is properly maintained
- Operations staff to plan production around maintenance schedules

## API Endpoints

The module provides the following API endpoints:
- `POST /equipment-maintenance/`: Create a new maintenance record
- `GET /equipment-maintenance/`: List maintenance records
- `GET /equipment-maintenance/{maintenance_id}`: Get a specific maintenance record
- `PUT /equipment-maintenance/{maintenance_id}`: Update a maintenance record
- `DELETE /equipment-maintenance/{maintenance_id}`: Delete a maintenance record
- `GET /equipment-maintenance/equipment/{equipment_id}`: Get maintenance history for equipment
- `POST /equipment-maintenance/{maintenance_id}/start`: Start a maintenance
- `POST /equipment-maintenance/{maintenance_id}/complete`: Complete a maintenance
- `POST /equipment-maintenance/{maintenance_id}/delay`: Delay a maintenance
- `POST /equipment-maintenance/{maintenance_id}/cancel`: Cancel a maintenance 