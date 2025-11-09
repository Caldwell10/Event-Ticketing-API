from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

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


if __name__ == "__main__":
    print(f"Working here: {DATABASE_URL}")
