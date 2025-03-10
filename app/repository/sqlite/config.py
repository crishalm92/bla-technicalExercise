from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (using a relative path for this example)
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session class to use throughout the application
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a SQLAlchemy Base
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def config_db():
    Base.metadata.create_all(bind=engine)
