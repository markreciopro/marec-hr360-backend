from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# 🆕 DATABASE IMPORTS
# We import the engine from your database.py and the Base from models.py
from database import engine
import models

# ✅ MAGIC COMMAND: This creates the tables in PostgreSQL automatically
# It looks at models.py and builds whatever is missing in your DB
models.Base.metadata.create_all(bind=engine)

# ✅ SETUP LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MAREC HR360 API")

# 🌐 CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ IMPORT & LINK ROUTERS
try:
    # Note: Using 'from .routes' if this main.py is inside an app folder, 
    # or just 'from routes' if it's in the root.
    from routes import dashboard, employees
    app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
    app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
    logger.info("🚀 All MAREC routes and Database connected successfully")
except ImportError as e:
    logger.error(f"❌ Import Error: {e}. Check your routes folder structure!")

@app.get("/")
def root():
    return {
        "message": "MAREC HR360 API is Live", 
        "owner": "MAREC Insights",
        "database": "PostgreSQL Connected"
    }