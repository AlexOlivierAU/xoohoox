# API Integration Guide

## Overview
The frontend is now fully integrated with the backend API. All major functionality is connected to the FastAPI endpoints.

## Services

### Authentication Service (`authService.ts`)
- **Login**: `POST /auth/token`
- **Get Current User**: `GET /auth/me`
- **Logout**: Local storage cleanup

### Batch Service (`batchService.ts`)
- **Get All Batches**: `GET /batches/`
- **Get Single Batch**: `GET /batches/{batch_id}`
- **Create Batch**: `POST /batches/`
- **Update Batch**: `PUT /batches/{batch_id}`
- **Delete Batch**: `DELETE /batches/{batch_id}`
- **Update Status**: `PATCH /batches/{batch_id}/status`
- **Start Batch**: `POST /batches/{batch_id}/start`
- **Complete Batch**: `POST /batches/{batch_id}/complete`
- **Quality Checks**: `GET /batches/{batch_id}/quality-checks`
- **Report Issues**: `POST /batches/{batch_id}/issues`
- **Corrective Actions**: `POST /batches/{batch_id}/corrective-actions`

### Quality Control Service (`qualityService.ts`)
- **Get All Checks**: `GET /quality-control/`
- **Get Single Check**: `GET /quality-control/{test_id}`
- **Create Check**: `POST /quality-control/`
- **Update Check**: `PUT /quality-control/{test_id}`
- **Delete Check**: `DELETE /quality-control/{test_id}`
- **Batch Checks**: `GET /quality-control/batch/{batch_id}`
- **Verify Check**: `POST /quality-control/{test_id}/verify`
- **Request Retest**: `POST /quality-control/{test_id}/request-retest`
- **Get Parameters**: `GET /quality-control/parameters`

## Authentication Flow

1. **Login**: User enters credentials → API call to `/auth/token` → Store token
2. **Protected Routes**: Check token on route access
3. **API Calls**: Include token in Authorization header
4. **Logout**: Clear local storage

## Environment Configuration

Create a `.env` file in the frontend root:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_NODE_ENV=development
```

## Error Handling

All API calls include:
- Loading states
- Error messages
- Retry logic
- Token refresh handling

## Testing the Integration

1. Start the backend server
2. Start the frontend: `pnpm dev`
3. Navigate to `/login`
4. Use demo credentials or create a user
5. Test all functionality

## Demo Credentials

For testing purposes, the backend accepts any credentials. In production, implement proper authentication. 