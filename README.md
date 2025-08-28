# XooHooX - Australian Laboratory Management System

A comprehensive laboratory management system for tracking research samples, geolocation monitoring, and quality control throughout the entire research lifecycle.

## 🧪 Overview

XooHooX is a full-stack application designed for Australian research laboratories to manage:
- **Research Sample Tracking**: End-to-end sample collection and processing
- **Geolocation Monitoring**: Farm mapping, geofencing, and sample collection tracking
- **Logistics & Delivery**: Real-time sample collection and laboratory delivery tracking
- **Quality Control**: Comprehensive quality monitoring and testing
- **Equipment Maintenance**: Preventive maintenance scheduling
- **Production Analytics**: Real-time monitoring and reporting

## 🏗️ Architecture

```
catalyst/
├── xoohoox-frontend/     # React + TypeScript + Vite (Main App)
├── xoohoox-backend/      # FastAPI + SQLAlchemy + PostgreSQL (API)
├── geolocation_dashboard.py    # Streamlit Geolocation Dashboard
├── logistics_tracking.py       # Streamlit Logistics Dashboard
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for caching)

### 1. Clone the Repository
```bash
git clone https://github.com/AlexOlivierAU/xoohoox.git
cd xoohoox
```

### 2. Backend Setup
```bash
cd xoohoox-backend/xoohoox-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Create PostgreSQL database and user
psql postgres -c "CREATE USER xoohoox WITH PASSWORD 'xoohoox123';"
psql postgres -c "CREATE DATABASE xoohoox OWNER xoohoox;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE xoohoox TO xoohoox;"

# Run migrations
alembic upgrade head
```

### 4. Frontend Setup
```bash
cd xoohoox-frontend
npm install
```

### 5. Start the Application
```bash
# Terminal 1 - Backend API
cd xoohoox-backend/xoohoox-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - React Frontend
cd xoohoox-frontend
npm run dev

# Terminal 3 - Geolocation Dashboard
cd /path/to/catalyst
streamlit run geolocation_dashboard.py --server.port 8501

# Terminal 4 - Logistics Dashboard
cd /path/to/catalyst
streamlit run logistics_tracking.py --server.port 8502
```

## 🌐 Access Points
- **React Frontend**: http://localhost:5173 (Main Laboratory Management System)
- **Backend API**: http://localhost:8000 (85+ API endpoints)
- **API Documentation**: http://localhost:8000/docs
- **Geolocation Dashboard**: http://localhost:8501 (Farm mapping & sample collection)
- **Logistics Dashboard**: http://localhost:8502 (Sample delivery tracking)

## 📋 Core Workflows

### 1. Research Sample Collection
- **Geolocation tracking** from Australian farms
- **Sample collection** with GPS coordinates
- **Batch creation** with unique identifiers
- **Quality assessment** during collection

### 2. Sample Processing & Analysis
- **Laboratory processing** workflow management
- **Quality control** testing and validation
- **Data recording** and analysis tracking
- **Result reporting** and documentation

### 3. Logistics & Delivery
- **Real-time tracking** of sample collection vehicles
- **Delivery monitoring** to laboratory facilities
- **Route optimization** and scheduling
- **Status updates** and notifications

### 4. Quality Control
- **Comprehensive testing** protocols
- **Equipment maintenance** scheduling
- **Real-time monitoring** dashboard
- **Compliance reporting** for Australian standards

## 🗺️ Geolocation Features

### Farm Management
- **Interactive maps** of Australian research farms
- **Geofencing** for sample collection zones
- **Real-time tracking** of sample collection
- **Weather monitoring** during collection

### Sample Collection Tracking
- **GPS coordinates** for all collection points
- **Collection timestamps** and metadata
- **Quality scores** and assessments
- **Batch linking** to collection locations

## 🚛 Logistics & Delivery

### Vehicle Tracking
- **Real-time location** of collection vehicles
- **Route optimization** and planning
- **Delivery scheduling** and ETA tracking
- **Status monitoring** and alerts

### Sample Delivery
- **End-to-end tracking** from farm to laboratory
- **Temperature monitoring** during transit
- **Quality preservation** protocols
- **Delivery confirmation** and documentation

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Material-UI (MUI)** for components
- **Vite** for build tooling
- **React Router** for navigation
- **Redux Toolkit** for state management

### Backend
- **FastAPI** for API framework
- **SQLAlchemy** for ORM
- **PostgreSQL** for database
- **Alembic** for migrations
- **Pydantic** for data validation

### Streamlit Dashboards
- **Folium** for interactive mapping
- **Plotly** for data visualization
- **Pandas** for data processing
- **Streamlit** for rapid dashboard development

### Development Tools
- **ESLint** for code linting
- **Prettier** for code formatting
- **Jest** for testing
- **Docker** for containerization

## 📁 Project Structure

```
catalyst/
├── xoohoox-frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components (20+ pages)
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API services
│   │   ├── store/         # Redux store
│   │   └── types/         # TypeScript definitions
│   ├── public/            # Static assets
│   └── package.json
├── xoohoox-backend/
│   ├── app/
│   │   ├── api/           # API endpoints (85+ endpoints)
│   │   ├── models/        # Database models (41 tables)
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── crud/          # Database operations
│   │   └── core/          # Configuration
│   ├── migrations/        # Database migrations
│   └── requirements.txt
├── geolocation_dashboard.py    # Farm mapping & sample collection
├── logistics_tracking.py       # Delivery & logistics tracking
└── README.md
```

## 🔧 Configuration

### Environment Variables
Create `.env` files in respective directories:

**Backend** (`xoohoox-backend/xoohoox-backend/.env`):
```env
DATABASE_URL=postgresql://xoohoox:xoohoox123@localhost:5432/xoohoox
SECRET_KEY=your-secret-key
DEBUG=True
```

**Frontend** (`xoohoox-frontend/.env`):
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

## 🧪 Testing

### Backend Tests
```bash
cd xoohoox-backend/xoohoox-backend
pytest
```

### Frontend Tests
```bash
cd xoohoox-frontend
npm test
```

## 📊 API Endpoints (85+ Total)

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Batch Management
- `GET /api/v1/batches` - List batches
- `POST /api/v1/batches` - Create batch
- `GET /api/v1/batches/{id}` - Get batch details
- `PUT /api/v1/batches/{id}` - Update batch

### Quality Control
- `GET /api/v1/quality-control` - List QC records
- `POST /api/v1/quality-control` - Create QC record

### Equipment Maintenance
- `GET /api/v1/maintenance` - List maintenance logs
- `POST /api/v1/maintenance` - Create maintenance log

### Mock Data (Development)
- `GET /api/v1/mock/batches` - Mock batch data
- `GET /api/v1/mock/quality-checks` - Mock QC data

## 🗺️ Australian Geographic Coverage

### Research Farms
- **Victoria**: Mildura region (Citrus research)
- **Tasmania**: Hobart region (Apple and grape research)
- **Queensland**: Cairns region (Tropical fruit research)
- **New South Wales**: Hunter Valley (Wine grape research)
- **Western Australia**: Margaret River (Premium fruit research)

### Sample Collection Zones
- **Geofenced areas** for precise collection tracking
- **Weather monitoring** during collection periods
- **Quality assessment** at collection points
- **Real-time GPS tracking** of collection activities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the [API Documentation](http://localhost:8000/docs) when running locally
- Review the [Streamlit Visualization Guide](STREAMLIT_VISUALIZATION.md)

## 🗺️ Roadmap

- [x] ✅ Geolocation tracking system
- [x] ✅ Logistics and delivery monitoring
- [x] ✅ Australian farm mapping
- [x] ✅ Real-time sample collection tracking
- [ ] Real-time WebSocket notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app support
- [ ] Integration with external laboratory systems
- [ ] Machine learning for quality prediction
- [ ] IoT sensor integration for environmental monitoring

---

**XooHooX** - Transforming Australian research through intelligent laboratory management 🧪🇦🇺
