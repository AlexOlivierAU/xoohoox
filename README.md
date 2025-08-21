# XooHooX - Juice Production Management System

A comprehensive juice production management system for tracking fermentation trials, batch processing, and quality control throughout the entire production lifecycle.

## 🍊 Overview

XooHooX is a full-stack application designed for juice production facilities to manage:
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

## 🎯 **Current Status: DATABASE COMPLETE** ✅

### **Database Schema: PRODUCTION READY**
- **Database**: PostgreSQL 14
- **Tables**: 41
- **Total Fields**: 553
- **Enum Types**: 14
- **Status**: ✅ Complete and Verified

### **Key Achievements:**
- ✅ Complete database schema with 553 fields
- ✅ All 41 tables properly structured
- ✅ 14 enum types for data integrity
- ✅ Foreign key relationships established
- ✅ Performance indexes created
- ✅ PostgreSQL production ready

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

# Recreate complete database schema (553 fields, 41 tables)
psql postgresql://postgres:postgres@localhost:5432/xoohoox -f recreate_schema.sql
psql postgresql://postgres:postgres@localhost:5432/xoohoox -f add_missing_tables.sql
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

## 📊 **Database Schema Overview**

### **Core Production Tables (8 tables)**
- `batch_tracking` (36 fields) - Main batch management
- `batch_dispatches` (7 fields) - Batch dispatch information
- `fermentation_trials` (17 fields) - Fermentation experiments
- `upscale_runs` (10 fields) - Production scaling
- `transformation_stages` (16 fields) - Production stages

### **Process Results (12 tables)**
- `juicing_results` (19 fields) - Juicing process results
- `chemistry_results` (13 fields) - Chemistry analysis
- `fermentation_results` (10 fields) - Fermentation outcomes
- `vinegar_results` (15 fields) - Vinegar production
- `distillation_results` (14 fields) - Distillation outcomes

### **Quality & Evaluation (6 tables)**
- `quality_control` (22 fields) - Quality testing
- `produce_prelim_eval` (17 fields) - Produce evaluation
- `product_evaluation` (11 fields) - Product evaluation
- `sensory_feedback` (13 fields) - Sensory feedback

### **Equipment & Maintenance (3 tables)**
- `equipment` (14 fields) - Equipment records
- `equipment_maintenance` (25 fields) - Maintenance tracking
- `inventory_management` (31 fields) - Stock tracking

### **Complete List**: 41 tables with 553 fields total

## 📋 Core Workflows

### **1. Batch Management**
```
Raw Material → Batch Creation → Quality Check → Processing → Final Product
```

### **2. Fermentation Trials**
```
Trial Setup → Yeast Inoculation → Daily Monitoring → Upscale Decision → Production
```

### **3. Quality Control**
```
Sample Collection → Testing → Results Recording → Decision Making → Action Items
```

### **4. Equipment Maintenance**
```
Scheduled Maintenance → Work Orders → Parts Tracking → Completion → Next Schedule
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

## 🔍 **Database Verification**

To verify the complete database schema:

```bash
# Check total counts
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "SELECT 'Tables: ' || COUNT(*)::text FROM information_schema.tables WHERE table_schema = 'public';"
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "SELECT 'Fields: ' || COUNT(*)::text FROM information_schema.columns WHERE table_schema = 'public';"

# List all tables
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "\dt"

# View table structure
psql postgresql://postgres:postgres@localhost:5432/xoohoox -c "\d table_name"
```

**Expected Results:**
- Tables: 41
- Fields: 553
- Enum Types: 14

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

- [x] Complete database schema (553 fields, 41 tables)
- [x] PostgreSQL production setup
- [ ] Real-time WebSocket notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app support
- [ ] Integration with external ERP systems
- [ ] Machine learning for quality prediction
- [ ] IoT sensor integration

## 🎉 **Project Status**

**Database**: ✅ **COMPLETE** - 553 fields across 41 tables  
**Backend**: 🚧 In Progress - FastAPI with complete data models  
**Frontend**: 🚧 In Progress - React with TypeScript  
**Documentation**: ✅ **COMPLETE** - Comprehensive schema documentation  

The database foundation is now complete and ready for full application development! 🚀
