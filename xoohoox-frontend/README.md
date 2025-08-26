# Xoohoox - Distillation Management System

A comprehensive web application for managing distillation, fermentation, and distillation processes. Built with React, TypeScript, and Material-UI for the frontend, and Python FastAPI for the backend.

## Features

- **Production Management**
  - Batch tracking and management
  - Real-time production monitoring
  - Quality control parameters
  - Equipment status tracking

- **Analytics & Reporting**
  - Production metrics and KPIs
  - Quality analytics
  - Equipment performance tracking
  - Custom report generation

- **Equipment Management**
  - Equipment status monitoring
  - Maintenance scheduling
  - Equipment type categorization
  - Critical equipment tracking

## Tech Stack

### Frontend
- React 18
- TypeScript
- Material-UI v5
- React Router v6
- Redux Toolkit (for state management)
- React Query (for API data fetching)
- Jest & React Testing Library (for testing)

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (for migrations)
- Pytest (for testing)

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- pnpm (recommended) or npm

### Frontend Setup
1. Install dependencies:
   ```bash
   cd xoohoox-frontend
   pnpm install
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Start development server:
   ```bash
   pnpm dev
   ```

### Backend Setup
1. Create virtual environment:
   ```bash
   cd xoohoox-backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Development

### Project Structure
```
xoohoox-frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── layouts/        # Layout components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── store/          # Redux store
│   ├── types/          # TypeScript types
│   └── utils/          # Utility functions
├── public/             # Static assets
└── tests/              # Test files

xoohoox-backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core functionality
│   ├── db/            # Database models
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
├── tests/             # Test files
└── alembic/           # Database migrations
```

### Code Style
- Frontend: ESLint + Prettier
- Backend: Black + isort + flake8

### Testing
- Frontend: `pnpm test`
- Backend: `pytest`

### Git Workflow
1. Create feature branch from `develop`
2. Make changes and commit
3. Create pull request to `develop`
4. Code review and merge

## Deployment

### Frontend Deployment
1. Build production assets:
   ```bash
   pnpm build
   ```

2. Deploy to hosting service (e.g., Vercel, Netlify)

### Backend Deployment
1. Set up production environment
2. Configure environment variables
3. Run migrations
4. Deploy using Docker or directly to server

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 