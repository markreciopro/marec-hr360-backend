from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# =========================
# FORCE LOAD ENV
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")

load_dotenv(env_path)

ENV = os.getenv("ENV", "local").lower()
LOCAL_DB = os.getenv("LOCAL_DB_URL")
CLOUD_DB = os.getenv("CLOUD_DB_URL")

# =========================
# VALIDATION (PREVENT CRASHES)
# =========================
if ENV == "cloud":
    if not CLOUD_DB:
        raise ValueError("❌ CLOUD_DB_URL is not set in .env")
    DATABASE_URL = CLOUD_DB
else:
    if not LOCAL_DB:
        raise ValueError("❌ LOCAL_DB_URL is not set in .env")
    DATABASE_URL = LOCAL_DB

# =========================
# ENGINE (AUTO SSL)
# =========================
if "localhost" in DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"}
    )

# =========================
# SESSION
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =========================
# DEBUG (CONFIRM WORKING)
# =========================
print(f"✅ ENV MODE: {ENV}")
print(f"✅ DATABASE_URL LOADED: {DATABASE_URL}")