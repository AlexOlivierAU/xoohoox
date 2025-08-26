# XooHooX - Distillation Management System

A comprehensive distillation management system for tracking fermentation trials, batch processing, and quality control throughout the entire production lifecycle.

## 🍊 Overview

XooHooX is a full-stack application designed for distillation facilities to manage:
- **Fermentation Trials**: Yeast strain testing and evaluation
- **Batch Processing**: End-to-end batch tracking from raw materials to finished product
- **Quality Control**: Comprehensive quality monitoring and testing
- **Equipment Maintenance**: Preventive maintenance scheduling
- **Production Analytics**: Real-time monitoring and reporting

## 🏗️ Architecture

```
catalyst/
├── xoohoox-frontend/     # React + TypeScript + Vite
├── xoohoox-backend/      # FastAPI + SQLAlchemy + PostgreSQL
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
# Terminal 1 - Backend
cd xoohoox-backend/xoohoox-backend
source venv/bin/activate
python run_dev.py

# Terminal 2 - Frontend
cd xoohoox-frontend
npm run dev
```

## 🌐 Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Core Workflows

### 1. Batch Creation & Planning
- Enhanced batch form with source tracking
- Batch ID format: `YYMMDD-FARMER-VARIETAL-XXX`
- Chemistry targets and byproduct tracking

### 2. Fermentation Management
- Yeast trial management and evaluation
- SG drop, EtOH, Brix monitoring
- Aroma and flocculation assessment

### 3. Upscaling Process
- Multi-stage upscaling (100L → 500L → 5000L)
- Progress tracking and stage management
- Quality control at each stage

### 4. Quality Control
- Compound analysis and sensory evaluation
- Equipment maintenance scheduling
- Real-time monitoring dashboard

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
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API services
│   │   ├── store/         # Redux store
│   │   └── types/         # TypeScript definitions
│   ├── public/            # Static assets
│   └── package.json
├── xoohoox-backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── crud/          # Database operations
│   │   └── core/          # Configuration
│   ├── migrations/        # Database migrations
│   └── requirements.txt
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
VITE_API_URL=http://localhost:8000
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

## 📊 API Endpoints

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

## 🗺️ Roadmap

- [ ] Real-time WebSocket notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app support
- [ ] Integration with external ERP systems
- [ ] Machine learning for quality prediction
- [ ] IoT sensor integration

---

**XooHooX** - Transforming juice production through intelligent management 🍊
