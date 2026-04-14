import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =========================
# ENV CONFIG
# =========================
ENV = os.getenv("ENV", "local")

LOCAL_DB = os.getenv("LOCAL_DB_URL")
CLOUD_DB = os.getenv("CLOUD_DB_URL")

# =========================
# SELECT DATABASE
# =========================
if ENV == "cloud" and CLOUD_DB:
    DB_URL = CLOUD_DB
    CONNECT_ARGS = {"sslmode": "require"}
    print("🌐 Using CLOUD database")
else:
    DB_URL = LOCAL_DB
    CONNECT_ARGS = {}
    print("💻 Using LOCAL database")

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
# BASE
# =========================
Base = declarative_base()


# =========================
# SAVE DATA (SMART)
# =========================
def save_data(df: pd.DataFrame, table_name="employees"):
    try:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"✅ Saved {len(df)} rows to {table_name}")
    except Exception as e:
        print("❌ Save error:", e)


# =========================
# LOAD DATA (SAFE)
# =========================
def load_data(table_name="employees"):
    try:
        return pd.read_sql(f"SELECT * FROM {table_name}", engine)
    except Exception as e:
        print("⚠️ Load error:", e)
        return pd.DataFrame()


# =========================
# OPTIONAL: CLOUD SYNC
# =========================
def sync_to_cloud(df: pd.DataFrame):
    if not CLOUD_DB:
        return

    try:
        cloud_engine = create_engine(
            CLOUD_DB,
            connect_args={"sslmode": "require"}
        )
        df.to_sql("employees", cloud_engine, if_exists="replace", index=False)
        print("☁️ Synced to cloud DB")
    except Exception as e:
        print("⚠️ Cloud sync failed:", e)