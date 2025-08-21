# Xoohoox Frontend Development Plan

## Overview
This document outlines the plan for developing the frontend of the Xoohoox Juice Production Management System using React, TypeScript, and Material-UI.

## Technical Stack
- **React 19**: For building the user interface
- **TypeScript**: For type safety and better developer experience
- **Material-UI v7**: For UI components and theming
- **Redux Toolkit**: For state management
- **React Query**: For data fetching and caching
- **Socket.io-client**: For real-time updates
- **Chart.js & MUI X-Charts**: For data visualization
- **React Router v6**: For navigation
- **Axios**: For HTTP requests
- **Jest & React Testing Library**: For testing

## Project Structure
```
xoohoox-frontend/
├── public/                  # Static assets
├── src/
│   ├── assets/              # Images, fonts, etc.
│   ├── components/          # Reusable UI components
│   │   ├── common/          # Common UI components
│   │   ├── layout/          # Layout components
│   │   ├── forms/           # Form components
│   │   ├── charts/          # Data visualization components
│   │   └── realtime/        # Real-time update components
│   ├── features/            # Feature-specific components
│   │   ├── auth/            # Authentication components
│   │   ├── batches/         # Batch management components
│   │   ├── quality/         # Quality control components
│   │   └── equipment/       # Equipment management components
│   ├── hooks/               # Custom React hooks
│   ├── pages/               # Page components
│   ├── services/            # API and service integrations
│   │   ├── api.ts           # API client setup
│   │   ├── authService.ts   # Authentication service
│   │   └── websocketService.ts # WebSocket service
│   ├── store/               # Redux store and slices
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions
│   ├── App.tsx              # Main application component
│   ├── index.tsx            # Application entry point
│   └── theme.ts             # Material-UI theme configuration
├── .env.development         # Development environment variables
├── .env.production          # Production environment variables
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
└── vite.config.ts           # Vite configuration
```

## Component Library

### Core Components
1. **Layout Components**
   - `AppLayout`: Main application layout
   - `Sidebar`: Navigation sidebar
   - `Header`: Application header
   - `Footer`: Application footer

2. **Common Components**
   - `Button`: Custom button component
   - `Card`: Card component for content
   - `Table`: Data table component
   - `Modal`: Modal dialog component
   - `Alert`: Alert/notification component
   - `Loading`: Loading indicator

3. **Form Components**
   - `TextField`: Text input field
   - `Select`: Dropdown select
   - `DatePicker`: Date selection
   - `TimePicker`: Time selection
   - `Checkbox`: Checkbox input
   - `Radio`: Radio button input
   - `FormSection`: Form section wrapper

4. **Visualization Components**
   - `LineChart`: Line chart for trends
   - `BarChart`: Bar chart for comparisons
   - `PieChart`: Pie chart for distributions
   - `GaugeChart`: Gauge for single metrics
   - `DataTable`: Tabular data with sorting/filtering

5. **Real-time Components**
   - `StatusIndicator`: Real-time status display
   - `LiveCounter`: Real-time counter
   - `NotificationBadge`: Real-time notification indicator
   - `LiveChart`: Real-time updating chart

### Feature Components
1. **Authentication**
   - `Login`: Login form
   - `Register`: Registration form
   - `ForgotPassword`: Password recovery
   - `ResetPassword`: Password reset

2. **Batch Management**
   - `BatchList`: List of batches
   - `BatchDetails`: Batch details view
   - `BatchForm`: Create/edit batch form
   - `BatchTimeline`: Batch process timeline
   - `BatchMetrics`: Batch performance metrics

3. **Quality Control**
   - `QualityDashboard`: Quality metrics dashboard
   - `QualityForm`: Quality data entry form
   - `QualityHistory`: Historical quality data
   - `QualityAlerts`: Quality alert notifications

4. **Equipment Management**
   - `EquipmentList`: List of equipment
   - `EquipmentDetails`: Equipment details view
   - `EquipmentStatus`: Real-time equipment status
   - `MaintenanceSchedule`: Maintenance scheduling
   - `MaintenanceHistory`: Maintenance history

## State Management

### Redux Store Structure
```
store/
├── index.ts                 # Store configuration
├── slices/
│   ├── authSlice.ts         # Authentication state
│   ├── batchSlice.ts        # Batch management state
│   ├── qualitySlice.ts      # Quality control state
│   ├── equipmentSlice.ts    # Equipment management state
│   └── uiSlice.ts           # UI state (modals, notifications)
└── hooks.ts                 # Redux hooks
```

### React Query Integration
- Use React Query for server state management
- Implement optimistic updates for better UX
- Configure caching strategies for different data types
- Handle loading and error states

### WebSocket State Management
- Implement WebSocket service for real-time updates
- Handle connection status and reconnection
- Manage subscriptions to different event types
- Update Redux store based on WebSocket events

## API Integration

### REST API Client
- Configure Axios instance with base URL and interceptors
- Implement authentication token management
- Handle request/response transformations
- Implement error handling and retry logic

### WebSocket Integration
- Connect to WebSocket server
- Handle connection events (connect, disconnect, error)
- Subscribe to relevant events
- Emit events to the server
- Handle reconnection logic

## Routing

### Route Structure
```
/                           # Dashboard
/login                      # Login page
/register                   # Registration page
/batches                    # Batch list
/batches/:id                # Batch details
/batches/new                # Create batch
/batches/:id/edit           # Edit batch
/quality                    # Quality dashboard
/quality/history            # Quality history
/equipment                  # Equipment list
/equipment/:id              # Equipment details
/equipment/maintenance      # Maintenance schedule
/settings                   # User settings
/profile                    # User profile
```

## Authentication Flow
1. User enters credentials on login page
2. Frontend sends credentials to authentication endpoint
3. Backend validates credentials and returns JWT token
4. Frontend stores token in secure storage
5. Token is included in subsequent API requests
6. Token is refreshed when expired
7. User is redirected to dashboard on successful login

## Data Visualization Strategy
### Chart Types
1. **Line Charts**
   - Temperature trends over time
   - pH level changes during fermentation
   - Sugar content reduction during fermentation
   - Alcohol content increase during fermentation

2. **Bar Charts**
   - Batch yield comparisons
   - Equipment utilization
   - Quality metrics by batch
   - Maintenance frequency by equipment

3. **Pie Charts**
   - Batch status distribution
   - Equipment status distribution
   - Quality issue distribution
   - Maintenance type distribution

4. **Gauge Charts**
   - Current temperature
   - Current pH level
   - Current sugar content
   - Current alcohol content

### Interactive Features
- Zoom and pan for time-series data
- Tooltips with detailed information
- Click-through to detailed views
- Real-time updates for active batches
- Customizable time ranges
- Export data functionality

## Real-time Updates Strategy
### WebSocket Events
1. **Batch Events**
   - `batch:created`: New batch created
   - `batch:updated`: Batch details updated
   - `batch:status_changed`: Batch status changed
   - `batch:completed`: Batch completed
   - `batch:quality_alert`: Quality alert for batch

2. **Equipment Events**
   - `equipment:status_changed`: Equipment status changed
   - `equipment:maintenance_due`: Maintenance due
   - `equipment:maintenance_completed`: Maintenance completed
   - `equipment:error`: Equipment error

3. **Quality Events**
   - `quality:measurement_recorded`: New quality measurement
   - `quality:threshold_exceeded`: Quality threshold exceeded
   - `quality:alert_triggered`: Quality alert triggered

### Update Frequencies
- Critical updates: Immediate
- Status changes: Every 30 seconds
- Metrics updates: Every 5 minutes
- Historical data: On demand

## Responsive Design
- Mobile-first approach
- Breakpoints for different device sizes
- Responsive layouts for all components
- Touch-friendly interactions for mobile
- Collapsible sidebar on smaller screens
- Stacked layouts for complex components on mobile

## Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast
- Focus management
- ARIA attributes where needed

## Performance Optimization
- Code splitting for routes
- Lazy loading for heavy components
- Memoization for expensive calculations
- Virtualization for long lists
- Image optimization
- Caching strategies for API data

## Testing Strategy
### Unit Tests
- Component rendering tests
- Hook tests
- Utility function tests
- Redux reducer tests
- API service tests

### Integration Tests
- User flow tests
- Form submission tests
- API integration tests
- WebSocket integration tests

### End-to-End Tests
- Critical user journeys
- Authentication flows
- Data entry workflows
- Real-time update scenarios

## Deployment Strategy
### Build Process
- Environment-specific builds
- Asset optimization
- Source map generation
- Bundle size analysis

### CI/CD Pipeline
- Automated testing
- Linting and type checking
- Build verification
- Automated deployment to staging/production

## Implementation Timeline
### Phase 1: Core Infrastructure (Week 1-2)
- Project setup and configuration
- Authentication implementation
- Basic layout and navigation
- API client setup
- WebSocket service implementation

### Phase 2: Batch Management (Week 3-4)
- Batch list and details views
- Batch creation and editing
- Batch timeline visualization
- Real-time batch updates

### Phase 3: Quality Control (Week 5-6)
- Quality dashboard
- Quality data entry forms
- Quality history views
- Quality alerts and notifications

### Phase 4: Equipment Management (Week 7-8)
- Equipment list and details
- Equipment status monitoring
- Maintenance scheduling
- Maintenance history

### Phase 5: Testing and Refinement (Week 9-10)
- Comprehensive testing
- Performance optimization
- Accessibility improvements
- Bug fixes and refinements

## Next Steps
1. Complete core feature implementation
- React 19
- TypeScript 5.0
- Material-UI v7
- Redux Toolkit for state management
- React Query for server state management
- Socket.io-client for real-time updates
- React Router v6 for routing
- Axios for HTTP requests
- Jest and React Testing Library for testing
- ESLint and Prettier for code quality

## Project Structure
```
src/
├── assets/           # Static assets (images, fonts, etc.)
├── components/       # Reusable UI components
│   ├── common/      # Common UI components
│   ├── layout/      # Layout components
│   ├── forms/       # Form components
│   └── charts/      # Chart components
├── features/        # Feature-specific components
│   ├── auth/        # Authentication
│   ├── batches/     # Batch management
│   ├── quality/     # Quality control
│   └── equipment/   # Equipment management
├── hooks/           # Custom React hooks
├── pages/           # Page components
├── services/        # API and WebSocket services
├── store/           # Redux store configuration
├── types/           # TypeScript type definitions
├── utils/           # Utility functions
└── tests/           # Test files
```

## Component Library

### Core Components
1. Layout Components
   - `AppLayout` - Main application layout
   - `Sidebar` - Navigation sidebar
   - `Header` - Application header
   - `Footer` - Application footer

2. Common Components
   - `Button` - Custom button component
   - `Input` - Form input component
   - `Select` - Dropdown select component
   - `Table` - Data table component
   - `Card` - Content card component
   - `Modal` - Dialog modal component
   - `Alert` - Notification alert component

3. Form Components
   - `Form` - Form wrapper component
   - `FormField` - Form field component
   - `FormSection` - Form section component
   - `ValidationMessage` - Form validation message

4. Visualization Components
   - `LineChart` - Time series data visualization
   - `BarChart` - Comparative data visualization
   - `GaugeChart` - Single value visualization
   - `StatusIndicator` - Status display component

5. Real-time Components
   - `WebSocketProvider` - WebSocket context provider
   - `RealTimeIndicator` - Connection status indicator
   - `LiveDataDisplay` - Real-time data display

### Feature Components
1. Authentication
   - `LoginForm` - User login form
   - `RegisterForm` - User registration form
   - `ForgotPasswordForm` - Password recovery form

2. Batch Management
   - `BatchList` - List of batches
   - `BatchDetails` - Batch details view
   - `BatchForm` - Batch creation/editing form
   - `BatchTimeline` - Batch progress timeline

3. Quality Control
   - `QualityCheckList` - List of quality checks
   - `QualityCheckForm` - Quality check form
   - `ParameterChart` - Parameter visualization
   - `AlertThresholds` - Alert threshold management

4. Equipment Management
   - `EquipmentList` - List of equipment
   - `EquipmentDetails` - Equipment details view
   - `MaintenanceSchedule` - Maintenance scheduling
   - `EquipmentStatus` - Equipment status display

## State Management

### Redux Store Structure
```typescript
interface RootState {
  auth: {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
  };
  batches: {
    items: Batch[];
    selectedBatch: Batch | null;
    loading: boolean;
    error: string | null;
  };
  quality: {
    checks: QualityCheck[];
    selectedCheck: QualityCheck | null;
    loading: boolean;
    error: string | null;
  };
  equipment: {
    items: Equipment[];
    selectedEquipment: Equipment | null;
    loading: boolean;
    error: string | null;
  };
  ui: {
    theme: 'light' | 'dark';
    sidebarOpen: boolean;
    notifications: Notification[];
  };
}
```

### React Query Integration
```typescript
// Example query hooks
const useBatches = () => useQuery('batches', fetchBatches);
const useBatch = (id: string) => useQuery(['batch', id], () => fetchBatch(id));
const useQualityChecks = (batchId: string) => 
  useQuery(['qualityChecks', batchId], () => fetchQualityChecks(batchId));
```

### WebSocket State Management
```typescript
// WebSocket context
interface WebSocketContextType {
  isConnected: boolean;
  connect: (url: string) => void;
  disconnect: () => void;
  subscribe: (event: string, callback: (data: any) => void) => void;
  unsubscribe: (event: string, callback: (data: any) => void) => void;
  emit: (event: string, data?: any) => boolean;
}
```

## API Integration

### REST API Client
```typescript
// api/client.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### WebSocket Client
```typescript
// services/websocketService.ts
import { io, Socket } from 'socket.io-client';
import { EventEmitter } from 'events';

class WebSocketService extends EventEmitter {
  private socket: Socket | null = null;
  private isConnected: boolean = false;

  public connect(url: string): void {
    this.socket = io(url, {
      query: { token: localStorage.getItem('token') },
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    });
  }

  public disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  public subscribe(event: string, callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  public unsubscribe(event: string, callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.off(event, callback);
    }
  }

  public emit(event: string, data?: any): boolean {
    if (this.socket) {
      this.socket.emit(event, data);
      return true;
    }
    return false;
  }
}
```

## Routing
```typescript
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<AppLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="batches">
          <Route index element={<BatchList />} />
          <Route path=":id" element={<BatchDetails />} />
          <Route path="new" element={<BatchForm />} />
        </Route>
        <Route path="quality">
          <Route index element={<QualityCheckList />} />
          <Route path=":id" element={<QualityCheckDetails />} />
        </Route>
        <Route path="equipment">
          <Route index element={<EquipmentList />} />
          <Route path=":id" element={<EquipmentDetails />} />
        </Route>
      </Route>
      <Route path="/auth">
        <Route path="login" element={<LoginForm />} />
        <Route path="register" element={<RegisterForm />} />
        <Route path="forgot-password" element={<ForgotPasswordForm />} />
      </Route>
    </Routes>
  </BrowserRouter>
);
```

## Authentication Flow
1. User enters credentials
2. Frontend sends login request
3. Backend validates and returns JWT
4. Frontend stores JWT in localStorage
5. Frontend redirects to dashboard
6. JWT is included in all subsequent requests
7. Token refresh handled automatically
8. Logout clears JWT and redirects to login

## Data Visualization Strategy
1. Chart Types
   - Line charts for time series data
   - Bar charts for comparative data
   - Gauge charts for single value metrics
   - Heat maps for parameter correlations

2. Interactive Features
   - Zoom and pan capabilities
   - Data point selection
   - Tooltip information
   - Export functionality

3. Real-time Updates
   - WebSocket integration
   - Smooth animations
   - Visual indicators for changes

## Real-time Updates Strategy
1. WebSocket Events
   - Connection management
   - Event subscription
   - Error handling
   - Reconnection logic

2. Update Frequencies
   - Critical data: Immediate
   - Status changes: 1-second delay
   - Metrics: 5-second delay
   - Historical data: On demand

3. State Management
   - Redux for UI state
   - React Query for server state
   - WebSocket for real-time updates

## Responsive Design
1. Breakpoints
   - Mobile: < 600px
   - Tablet: 600px - 960px
   - Desktop: > 960px

2. Layout Adaptations
   - Collapsible sidebar
   - Responsive tables
   - Adaptive charts
   - Mobile-friendly forms

## Accessibility
1. WCAG 2.1 Compliance
   - Keyboard navigation
   - Screen reader support
   - Color contrast
   - Focus management

2. Features
   - ARIA labels
   - Semantic HTML
   - Skip links
   - Error announcements

## Performance Optimization
1. Code Splitting
   - Route-based splitting
   - Component lazy loading
   - Dynamic imports

2. Caching Strategy
   - API response caching
   - Static asset caching
   - State persistence

3. Bundle Optimization
   - Tree shaking
   - Code minification
   - Asset compression

## Testing Strategy
1. Unit Tests
   - Component testing
   - Hook testing
   - Utility function testing

2. Integration Tests
   - Feature testing
   - API integration testing
   - WebSocket testing

3. End-to-End Tests
   - User flow testing
   - Cross-browser testing
   - Performance testing

## Deployment Strategy
1. CI/CD Pipeline
   - GitHub Actions
   - Automated testing
   - Build optimization
   - Deployment automation

2. Environments
   - Development
   - Staging
   - Production

3. Monitoring
   - Error tracking
   - Performance monitoring
   - User analytics

## Implementation Timeline
1. Phase 1: Core Setup (Week 1)
   - Project initialization
   - Component library setup
   - Routing configuration
   - State management setup

2. Phase 2: Authentication (Week 2)
   - Login/Register forms
   - JWT integration
   - Protected routes
   - User management

3. Phase 3: Batch Management (Weeks 3-4)
   - Batch list view
   - Batch details view
   - Batch creation/editing
   - Quality check integration

4. Phase 4: Quality Control (Weeks 5-6)
   - Quality check forms
   - Parameter visualization
   - Alert management
   - Real-time updates

5. Phase 5: Equipment Management (Weeks 7-8)
   - Equipment list view
   - Equipment details
   - Maintenance scheduling
   - Status monitoring

6. Phase 6: Polish & Deploy (Weeks 9-10)
   - Performance optimization
   - Testing & bug fixes
   - Documentation
   - Deployment

## Next Steps
1. Complete core feature implementation
2. Integrate real-time updates
3. Set up testing infrastructure
4. Deploy to staging environment
5. Gather feedback and iterate
6. Deploy to production 