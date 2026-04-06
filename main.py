from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# 🆕 DATABASE IMPORTS
from database import engine
import models

# ✅ MAGIC COMMAND: Creates tables in PostgreSQL (Local or Render) automatically
models.Base.metadata.create_all(bind=engine)

# ✅ SETUP LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MAREC HR360 API")

# 🌐 SURGICAL CORS CONFIG
# Adding your specific GitHub Pages URL to ensure the handshake works
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://markreciopro.github.io",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "*" 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ IMPORT & LINK ROUTERS
try:
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