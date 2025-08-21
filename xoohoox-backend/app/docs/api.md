# API Documentation

## Overview
This document provides information about the available API endpoints in the Xoohoox Backend.

## Authentication
All endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer YOUR_TOKEN
```

## Endpoints

### Users
- `GET /users/` - List all users
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

### Batches
- `GET /batches/` - List all batches
- `POST /batches/` - Create a new batch
- `GET /batches/{batch_id}` - Get a specific batch
- `PUT /batches/{batch_id}` - Update a batch
- `DELETE /batches/{batch_id}` - Delete a batch

### Maintenance Logs
- `GET /maintenance-logs/` - List all maintenance logs
- `POST /maintenance-logs/` - Create a new maintenance log
- `GET /maintenance-logs/{maintenance_log_id}` - Get a specific maintenance log
- `PUT /maintenance-logs/{maintenance_log_id}` - Update a maintenance log
- `DELETE /maintenance-logs/{maintenance_log_id}` - Delete a maintenance log
- `GET /maintenance-logs/maintenance/{maintenance_id}` - Get logs by maintenance ID
- `GET /maintenance-logs/technician/{technician_id}` - Get logs by technician ID

## Response Formats

### Success Response
```json
{
  "status": "success",
  "data": {
    // Response data
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "details": {
    // Additional error details
  }
}
```

## Pagination
Endpoints that return lists support pagination using the following query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

## Rate Limiting
API requests are limited to 100 requests per minute per IP address.

## Versioning
The API is versioned using the URL path: `/api/v1/`

## WebSocket Support
Some endpoints support real-time updates via WebSocket connections. See the WebSocket documentation for details. 