#!/usr/bin/env python3
"""
Simple database initialization script for Xoohoox Juice Production Management System
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.models.base import Base

def init_database():
    """Initialize the database with tables"""
    
    # Create engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")
    print(f"Database file: {settings.SQLALCHEMY_DATABASE_URI}")

if __name__ == "__main__":
    init_database() 