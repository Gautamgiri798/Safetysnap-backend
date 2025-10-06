from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# Get the database URL from environment variables
# We provide a default SQLite URL for local development if the variable isn't set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./safetysnap.db")

engine = create_engine(DATABASE_URL)

# For SQLite only, we need to add this argument
# if "sqlite" in DATABASE_URL:
#     engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# else:
#     engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()