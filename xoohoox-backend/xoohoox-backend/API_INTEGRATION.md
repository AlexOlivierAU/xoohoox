# Xoohoox API Integration Guide

## Overview

This document provides a comprehensive guide for integrating with the Xoohoox Juice Production Management System API. The API follows RESTful principles and includes WebSocket endpoints for real-time updates.

## Base URL

- Development: `http://localhost:8000/api/v1`
- Production: `https://api.xoohoox.com/api/v1`
- WebSocket: `ws://localhost:8000/ws` (Development) or `wss://api.xoohoox.com/ws` (Production)

## Authentication

The API uses JWT (JSON Web Token) for authentication. To authenticate, include the token in the Authorization header:

```
Authorization: Bearer <token>
```

### Authentication Endpoints

#### Login

```
POST /auth/login
```

Request body:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Register

```
POST /auth/register
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-04-12T12:00:00Z",
  "updated_at": "2023-04-12T12:00:00Z"
}
```

#### Refresh Token

```
POST /auth/refresh
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Batch Management

### List Batches

```
GET /batches
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `status`: Filter by status (active, completed, etc.)
- `start_date`: Filter by start date
- `end_date`: Filter by end date

Response:
```json
{
  "items": [
    {
      "id": 1,
      "name": "Batch-2023-001",
      "status": "active",
      "start_date": "2023-04-12T12:00:00Z",
      "end_date": null,
      "created_at": "2023-04-12T12:00:00Z",
      "updated_at": "2023-04-12T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

### Get Batch Details

```
GET /batches/{batch_id}
```

Response:
```json
{
  "id": 1,
  "name": "Batch-2023-001",
  "status": "active",
  "start_date": "2023-04-12T12:00:00Z",
  "end_date": null,
  "created_at": "2023-04-12T12:00:00Z",
  "updated_at": "2023-04-12T12:00:00Z",
  "metrics": {
    "temperature": 25.5,
    "ph": 3.2,
    "sugar_content": 12.5,
    "alcohol_content": 0.0
  },
  "quality_checks": [
    {
      "id": 1,
      "timestamp": "2023-04-12T12:00:00Z",
      "temperature": 25.5,
      "ph": 3.2,
      "sugar_content": 12.5,
      "alcohol_content": 0.0,
      "notes": "Initial measurement"
    }
  ]
}
```

### Create Batch

```
POST /batches
```

Request body:
```json
{
  "name": "Batch-2023-002",
  "start_date": "2023-04-13T12:00:00Z"
}
```

Response:
```json
{
  "id": 2,
  "name": "Batch-2023-002",
  "status": "active",
  "start_date": "2023-04-13T12:00:00Z",
  "end_date": null,
  "created_at": "2023-04-13T12:00:00Z",
  "updated_at": "2023-04-13T12:00:00Z"
}
```

### Update Batch

```
PUT /batches/{batch_id}
```

Request body:
```json
{
  "name": "Batch-2023-002-Updated",
  "status": "completed",
  "end_date": "2023-04-20T12:00:00Z"
}
```

Response:
```json
{
  "id": 2,
  "name": "Batch-2023-002-Updated",
  "status": "completed",
  "start_date": "2023-04-13T12:00:00Z",
  "end_date": "2023-04-20T12:00:00Z",
  "created_at": "2023-04-13T12:00:00Z",
  "updated_at": "2023-04-20T12:00:00Z"
}
```

### Delete Batch

```
DELETE /batches/{batch_id}
```

Response:
```json
{
  "message": "Batch deleted successfully"
}
```

## Quality Control

### Record Quality Check

```
POST /batches/{batch_id}/quality-checks
```

Request body:
```json
{
  "temperature": 25.5,
  "ph": 3.2,
  "sugar_content": 12.5,
  "alcohol_content": 0.0,
  "notes": "Daily quality check"
}
```

Response:
```json
{
  "id": 2,
  "batch_id": 1,
  "timestamp": "2023-04-12T12:00:00Z",
  "temperature": 25.5,
  "ph": 3.2,
  "sugar_content": 12.5,
  "alcohol_content": 0.0,
  "notes": "Daily quality check"
}
```

### Get Quality History

```
GET /batches/{batch_id}/quality-checks
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `start_date`: Filter by start date
- `end_date`: Filter by end date

Response:
```json
{
  "items": [
    {
      "id": 1,
      "batch_id": 1,
      "timestamp": "2023-04-12T12:00:00Z",
      "temperature": 25.5,
      "ph": 3.2,
      "sugar_content": 12.5,
      "alcohol_content": 0.0,
      "notes": "Initial measurement"
    },
    {
      "id": 2,
      "batch_id": 1,
      "timestamp": "2023-04-12T12:00:00Z",
      "temperature": 25.5,
      "ph": 3.2,
      "sugar_content": 12.5,
      "alcohol_content": 0.0,
      "notes": "Daily quality check"
    }
  ],
  "total": 2,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

## Equipment Management

### List Equipment

```
GET /equipment
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `status`: Filter by status (active, maintenance, etc.)
- `type`: Filter by equipment type

Response:
```json
{
  "items": [
    {
      "id": 1,
      "name": "Fermenter-001",
      "type": "fermenter",
      "status": "active",
      "last_maintenance": "2023-04-01T12:00:00Z",
      "next_maintenance": "2023-05-01T12:00:00Z",
      "created_at": "2023-04-01T12:00:00Z",
      "updated_at": "2023-04-01T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

### Get Equipment Details

```
GET /equipment/{equipment_id}
```

Response:
```json
{
  "id": 1,
  "name": "Fermenter-001",
  "type": "fermenter",
  "status": "active",
  "last_maintenance": "2023-04-01T12:00:00Z",
  "next_maintenance": "2023-05-01T12:00:00Z",
  "created_at": "2023-04-01T12:00:00Z",
  "updated_at": "2023-04-01T12:00:00Z",
  "maintenance_history": [
    {
      "id": 1,
      "equipment_id": 1,
      "date": "2023-04-01T12:00:00Z",
      "type": "routine",
      "description": "Routine maintenance",
      "technician": "John Doe",
      "notes": "All systems functioning normally"
    }
  ]
}
```

### Update Equipment Status

```
PUT /equipment/{equipment_id}/status
```

Request body:
```json
{
  "status": "maintenance",
  "notes": "Scheduled maintenance"
}
```

Response:
```json
{
  "id": 1,
  "name": "Fermenter-001",
  "type": "fermenter",
  "status": "maintenance",
  "last_maintenance": "2023-04-01T12:00:00Z",
  "next_maintenance": "2023-05-01T12:00:00Z",
  "created_at": "2023-04-01T12:00:00Z",
  "updated_at": "2023-04-01T12:00:00Z"
}
```

### Record Maintenance

```
POST /equipment/{equipment_id}/maintenance
```

Request body:
```json
{
  "date": "2023-04-01T12:00:00Z",
  "type": "routine",
  "description": "Routine maintenance",
  "technician": "John Doe",
  "notes": "All systems functioning normally"
}
```

Response:
```json
{
  "id": 1,
  "equipment_id": 1,
  "date": "2023-04-01T12:00:00Z",
  "type": "routine",
  "description": "Routine maintenance",
  "technician": "John Doe",
  "notes": "All systems functioning normally"
}
```

## WebSocket Integration

The WebSocket API provides real-time updates for various events in the system.

### Connection

Connect to the WebSocket server:

```javascript
const socket = io('ws://localhost:8000/ws', {
  auth: {
    token: 'your_jwt_token'
  }
});
```

### Events

#### Batch Events

- `batch:created`: Emitted when a new batch is created
  ```json
  {
    "id": 2,
    "name": "Batch-2023-002",
    "status": "active",
    "start_date": "2023-04-13T12:00:00Z",
    "end_date": null,
    "created_at": "2023-04-13T12:00:00Z",
    "updated_at": "2023-04-13T12:00:00Z"
  }
  ```

- `batch:updated`: Emitted when a batch is updated
  ```json
  {
    "id": 2,
    "name": "Batch-2023-002-Updated",
    "status": "completed",
    "start_date": "2023-04-13T12:00:00Z",
    "end_date": "2023-04-20T12:00:00Z",
    "created_at": "2023-04-13T12:00:00Z",
    "updated_at": "2023-04-20T12:00:00Z"
  }
  ```

- `batch:status_changed`: Emitted when a batch status changes
  ```json
  {
    "id": 2,
    "status": "completed",
    "previous_status": "active"
  }
  ```

- `batch:quality_alert`: Emitted when a quality alert is triggered
  ```json
  {
    "batch_id": 1,
    "alert_type": "temperature_high",
    "value": 30.5,
    "threshold": 28.0,
    "timestamp": "2023-04-12T12:00:00Z"
  }
  ```

#### Equipment Events

- `equipment:status_changed`: Emitted when equipment status changes
  ```json
  {
    "id": 1,
    "status": "maintenance",
    "previous_status": "active"
  }
  ```

- `equipment:maintenance_due`: Emitted when maintenance is due
  ```json
  {
    "id": 1,
    "name": "Fermenter-001",
    "next_maintenance": "2023-05-01T12:00:00Z",
    "days_until_maintenance": 5
  }
  ```

- `equipment:maintenance_completed`: Emitted when maintenance is completed
  ```json
  {
    "id": 1,
    "maintenance_id": 1,
    "date": "2023-04-01T12:00:00Z",
    "type": "routine",
    "technician": "John Doe"
  }
  ```

- `equipment:error`: Emitted when equipment error occurs
  ```json
  {
    "id": 1,
    "error_type": "temperature_sensor_failure",
    "description": "Temperature sensor not responding",
    "timestamp": "2023-04-12T12:00:00Z"
  }
  ```

#### Quality Events

- `quality:measurement_recorded`: Emitted when a quality measurement is recorded
  ```json
  {
    "id": 2,
    "batch_id": 1,
    "timestamp": "2023-04-12T12:00:00Z",
    "temperature": 25.5,
    "ph": 3.2,
    "sugar_content": 12.5,
    "alcohol_content": 0.0,
    "notes": "Daily quality check"
  }
  ```

- `quality:threshold_exceeded`: Emitted when a quality threshold is exceeded
  ```json
  {
    "batch_id": 1,
    "metric": "temperature",
    "value": 30.5,
    "threshold": 28.0,
    "timestamp": "2023-04-12T12:00:00Z"
  }
  ```

### Subscribing to Events

To subscribe to specific events:

```javascript
// Subscribe to batch events
socket.on('batch:created', (data) => {
  console.log('New batch created:', data);
});

socket.on('batch:updated', (data) => {
  console.log('Batch updated:', data);
});

// Subscribe to equipment events
socket.on('equipment:status_changed', (data) => {
  console.log('Equipment status changed:', data);
});

// Subscribe to quality events
socket.on('quality:measurement_recorded', (data) => {
  console.log('Quality measurement recorded:', data);
});
```

### Emitting Events

To emit events to the server:

```javascript
// Update batch status
socket.emit('batch:update_status', {
  batch_id: 1,
  status: 'completed'
});

// Record quality measurement
socket.emit('quality:record_measurement', {
  batch_id: 1,
  temperature: 25.5,
  ph: 3.2,
  sugar_content: 12.5,
  alcohol_content: 0.0,
  notes: 'Daily quality check'
});
```

## Error Handling

The API uses standard HTTP status codes and returns error messages in a consistent format:

```json
{
  "detail": "Error message description"
}
```

Common error codes:
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Rate Limiting

The API implements rate limiting to prevent abuse. The current limits are:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in the response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1618234567
```

## Pagination

List endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

The response includes pagination metadata:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10,
  "pages": 10
}
```

## Filtering and Sorting

List endpoints support filtering and sorting with query parameters:

### Filtering

- `status`: Filter by status
- `start_date`: Filter by start date
- `end_date`: Filter by end date
- `type`: Filter by type

### Sorting

- `sort`: Field to sort by (e.g., `created_at`, `name`)
- `order`: Sort order (`asc` or `desc`, default: `desc`)

Example:
```
GET /batches?status=active&sort=created_at&order=desc
```

## Versioning

The API is versioned using the URL path: `/api/v1/`. Breaking changes will be introduced in new versions (e.g., `/api/v2/`).

## SDKs and Libraries

Official SDKs and libraries are available for the following languages:
- JavaScript/TypeScript: `xoohoox-js`
- Python: `xoohoox-py`
- Java: `xoohoox-java`

## Support

For API support, please contact:
- Email: api-support@xoohoox.com
- Documentation: https://docs.xoohoox.com/api
- Status page: https://status.xoohoox.com 