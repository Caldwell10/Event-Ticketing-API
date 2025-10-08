from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load environement variable from .env file to prevent exposing sensitive DB credentials
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/event_ticketing"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a Session instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for class definitions
Base = declarative_base()

# Initialize dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



