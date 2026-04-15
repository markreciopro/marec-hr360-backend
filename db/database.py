import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# =========================
# ENVIRONMENT CONFIG
# =========================

ENV = os.getenv("ENV", "local")

LOCAL_DB_URL = os.getenv("LOCAL_DB_URL")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# =========================
# SELECT DATABASE
# =========================

if ENV == "cloud" and SUPABASE_DB_URL:
    DB_URL = SUPABASE_DB_URL
    CONNECT_ARGS = {"sslmode": "require"}
    print("🌐 Using SUPABASE cloud database")
else:
    DB_URL = LOCAL_DB_URL
    CONNECT_ARGS = {}
    print("💻 Using LOCAL PostgreSQL database")

# =========================
# ENGINE
# =========================

engine = create_engine(
    DB_URL,
    connect_args=CONNECT_ARGS,
    pool_pre_ping=True
)

# =========================
# SESSION
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
