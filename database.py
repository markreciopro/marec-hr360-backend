# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 🔥 UPDATE THIS
DATABASE_URL = "postgresql://postgres:password@localhost:5432/marec_db"

# Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Session (optional for future ORM use)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)