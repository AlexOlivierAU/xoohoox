# API Integration Documentation

## Overview
This document outlines the API integration strategy for the Xoohoox Juice Production Management System, including both REST API endpoints and WebSocket connections for real-time updates.

## REST API Integration

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
- JWT-based authentication
- Token included in Authorization header
- Format: `Bearer <token>`

### Endpoints

#### Authentication
- POST /auth/login
- POST /auth/register
- POST /auth/refresh
- POST /auth/logout

#### Batch Management
- GET /batches
- POST /batches
- GET /batches/{id}
- PUT /batches/{id}
- DELETE /batches/{id}
- GET /batches/{id}/quality
- GET /batches/{id}/equipment

#### Quality Control
- GET /quality
- POST /quality
- GET /quality/{id}
- PUT /quality/{id}
- DELETE /quality/{id}
- GET /quality/batch/{batch_id}

#### Equipment Maintenance
- GET /equipment
- POST /equipment
- GET /equipment/{id}
- PUT /equipment/{id}
- DELETE /equipment/{id}
- GET /equipment/maintenance
- POST /equipment/maintenance

### Request/Response Format
- Content-Type: application/json
- Response format:
```json
{
  "status": "success",
  "data": {},
  "message": "Operation successful"
}
```

### Error Handling
- HTTP status codes
- Error response format:
```json
{
  "status": "error",
  "message": "Error description",
  "errors": []
}
```

## WebSocket Integration

### Connection
- WebSocket URL: `ws://localhost:8000/ws`
- Connection established after authentication
- Automatic reconnection on disconnection

### Events

#### Client to Server
- `auth`: Send authentication token
- `subscribe`: Subscribe to specific channels
- `unsubscribe`: Unsubscribe from channels
- `ping`: Keep connection alive

#### Server to Client
- `batchUpdate`: Batch status changes
  ```json
  {
    "event": "batchUpdate",
    "data": {
      "batch_id": "string",
      "status": "string",
      "updated_at": "string"
    }
  }
  ```
- `qualityAlert`: Quality control issues
  ```json
  {
    "event": "qualityAlert",
    "data": {
      "batch_id": "string",
      "parameter": "string",
      "value": "number",
      "threshold": "number",
      "severity": "string"
    }
  }
  ```
- `equipmentStatus`: Equipment status changes
  ```json
  {
    "event": "equipmentStatus",
    "data": {
      "equipment_id": "string",
      "status": "string",
      "last_maintenance": "string",
      "next_maintenance": "string"
    }
  }
  ```
- `inventoryUpdate`: Inventory level changes
  ```json
  {
    "event": "inventoryUpdate",
    "data": {
      "item_id": "string",
      "quantity": "number",
      "threshold": "number"
    }
  }
  ```
- `systemAlert`: System-wide alerts
  ```json
  {
    "event": "systemAlert",
    "data": {
      "type": "string",
      "message": "string",
      "severity": "string"
    }
  }
  ```

### Channels
- `batches`: Batch-related updates
- `quality`: Quality control updates
- `equipment`: Equipment status updates
- `inventory`: Inventory level updates
- `system`: System-wide alerts

### Connection Management
- Heartbeat interval: 30 seconds
- Reconnection attempts: 5
- Reconnection delay: Exponential backoff
- Maximum delay: 30 seconds

### Error Handling
- Connection errors
- Authentication errors
- Subscription errors
- Message parsing errors

## Data Models

### Batch
```typescript
interface Batch {
  id: string;
  product_type: string;
  quantity: number;
  start_date: string;
  expected_completion_date: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  quality_checks: QualityCheck[];
  equipment_used: Equipment[];
}
```

### Quality Check
```typescript
interface QualityCheck {
  id: string;
  batch_id: string;
  parameter: string;
  value: number;
  threshold: number;
  timestamp: string;
  status: 'pass' | 'fail' | 'warning';
}
```

### Equipment
```typescript
interface Equipment {
  id: string;
  name: string;
  type: string;
  status: 'operational' | 'maintenance' | 'failed';
  last_maintenance: string;
  next_maintenance: string;
  maintenance_history: MaintenanceRecord[];
}
```

### Maintenance Record
```typescript
interface MaintenanceRecord {
  id: string;
  equipment_id: string;
  type: 'preventive' | 'corrective';
  description: string;
  technician: string;
  start_date: string;
  end_date: string;
  status: 'scheduled' | 'in_progress' | 'completed';
  cost: number;
}
```

## Integration Examples

### REST API Example
```typescript
// Create a new batch
const createBatch = async (batchData: Partial<Batch>) => {
  const response = await axios.post('/api/v1/batches', batchData, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
```

### WebSocket Example
```typescript
// Subscribe to batch updates
const subscribeToBatches = (socket: Socket) => {
  socket.emit('subscribe', { channel: 'batches' });
  
  socket.on('batchUpdate', (data) => {
    // Handle batch update
    console.log('Batch updated:', data);
  });
};
```

## Error Handling Examples

### REST API Error
```typescript
try {
  const response = await axios.get('/api/v1/batches/123');
} catch (error) {
  if (axios.isAxiosError(error)) {
    if (error.response?.status === 404) {
      // Handle not found
    } else if (error.response?.status === 401) {
      // Handle unauthorized
    }
  }
}
```

### WebSocket Error
```typescript
socket.on('error', (error) => {
  if (error.type === 'auth') {
    // Handle authentication error
  } else if (error.type === 'connection') {
    // Handle connection error
  }
});
```

## Best Practices
1. Always include error handling
2. Implement retry logic for failed requests
3. Use appropriate HTTP methods
4. Validate request/response data
5. Handle WebSocket disconnections gracefully
6. Implement proper cleanup on component unmount
7. Use TypeScript interfaces for type safety
8. Document all API changes
9. Version your APIs
10. Monitor API performance and errors

## Security Considerations
1. Use HTTPS for REST API
2. Use WSS for WebSocket connections
3. Implement rate limiting
4. Validate all input data
5. Sanitize output data
6. Use proper authentication
7. Implement proper authorization
8. Log security events
9. Monitor for suspicious activity
10. Keep dependencies updated

## Testing
1. Unit tests for API clients
2. Integration tests for API endpoints
3. WebSocket connection tests
4. Error handling tests
5. Authentication tests
6. Authorization tests
7. Rate limiting tests
8. Performance tests
9. Security tests
10. End-to-end tests 