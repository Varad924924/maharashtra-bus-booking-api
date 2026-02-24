from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This will create a file named "bus_booking.db" in your project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./bus_booking.db"

# 1. Create the engine (The connection to the file)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2. Create the Session (The tool to talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Base (The blueprint for our tables)
Base = declarative_base()

# 4. Dependency (We use this in every request to open/close the DB)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()