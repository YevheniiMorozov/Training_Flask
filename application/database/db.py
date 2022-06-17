from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USER = "postgres"
DB_PASS = 1488
IP = "127.0.0.1"
DB_NAME = "students"

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"

engine = create_engine(POSTGRES_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

