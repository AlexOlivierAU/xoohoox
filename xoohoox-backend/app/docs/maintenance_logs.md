# Maintenance Logs Module

## Overview
The Maintenance Logs module provides functionality for tracking and managing maintenance activities in the juice production system. It allows technicians to record maintenance actions, parts replaced, and associated costs for equipment maintenance.

## Models

### MaintenanceLog
The core model for tracking maintenance activities:

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| maintenance_id | Integer | Foreign key to Maintenance record |
| technician_id | Integer | Foreign key to User (technician) |
| action_taken | String | Description of maintenance action performed |
| notes | String | Additional notes about the maintenance |
| parts_replaced | String | List of parts replaced during maintenance |
| cost | Float | Cost associated with the maintenance |
| created_at | DateTime | Timestamp of record creation |
| updated_at | DateTime | Timestamp of last update |

## API Endpoints

### GET /maintenance-logs/
Retrieve all maintenance logs with pagination.

**Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "maintenance_id": 1,
    "technician_id": 1,
    "action_taken": "Replaced filter",
    "notes": "Regular maintenance",
    "parts_replaced": "Air filter",
    "cost": 50.0,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

### POST /maintenance-logs/
Create a new maintenance log.

**Request Body:**
```json
{
  "maintenance_id": 1,
  "technician_id": 1,
  "action_taken": "Replaced filter",
  "notes": "Regular maintenance",
  "parts_replaced": "Air filter",
  "cost": 50.0
}
```

**Response:** Created maintenance log object

### PUT /maintenance-logs/{maintenance_log_id}
Update an existing maintenance log.

**Parameters:**
- `maintenance_log_id` (int): ID of the maintenance log to update

**Request Body:**
```json
{
  "action_taken": "Updated action",
  "notes": "Updated notes",
  "parts_replaced": "Updated parts",
  "cost": 150.0
}
```

**Response:** Updated maintenance log object

### GET /maintenance-logs/{maintenance_log_id}
Retrieve a specific maintenance log by ID.

**Parameters:**
- `maintenance_log_id` (int): ID of the maintenance log to retrieve

**Response:** Maintenance log object

### DELETE /maintenance-logs/{maintenance_log_id}
Delete a maintenance log.

**Parameters:**
- `maintenance_log_id` (int): ID of the maintenance log to delete

**Response:** Deleted maintenance log object

### GET /maintenance-logs/maintenance/{maintenance_id}
Retrieve maintenance logs filtered by maintenance ID.

**Parameters:**
- `maintenance_id` (int): ID of the maintenance to filter by
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:** List of maintenance log objects

### GET /maintenance-logs/technician/{technician_id}
Retrieve maintenance logs filtered by technician ID.

**Parameters:**
- `technician_id` (int): ID of the technician to filter by
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:** List of maintenance log objects

## Authentication
All endpoints require authentication. Some operations (create, update, delete) require superuser privileges.

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Examples

### Creating a Maintenance Log
```python
import requests

url = "http://localhost:8000/api/v1/maintenance-logs/"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "maintenance_id": 1,
    "technician_id": 1,
    "action_taken": "Replaced filter",
    "notes": "Regular maintenance",
    "parts_replaced": "Air filter",
    "cost": 50.0
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Retrieving Maintenance Logs by Maintenance ID
```python
import requests

url = "http://localhost:8000/api/v1/maintenance-logs/maintenance/1"
headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}

response = requests.get(url, headers=headers)
print(response.json())
``` 