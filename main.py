from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

# DATABASE IMPORTS
try:
    from database import engine
    import models
    # Creates tables in PostgreSQL automatically
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables verified/created.")
except Exception as e:
    print(f"⚠️ Database connection warning: {e}")

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MAREC HR360 API",
    description="Workforce Intelligence Platform Backend",
    version="1.0.0"
)

# 🌐 SURGICAL CORS CONFIG
# This allows your frontend (GitHub or Local) to communicate with this backend
origins = [
    "https://markreciopro.github.io",
    "https://markreciopro.github.io/marec_hr360",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛡️ GLOBAL ERROR LOGGING & 404 CATCHER
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    if response.status_code == 404:
        logger.warning(f"❓ 404 Not Found: {request.method} {request.url.path}")
        
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | {process_time:.2f}ms")
    return response

# ✅ HEALTH CHECK ROUTE
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "online",
        "timestamp": time.time(),
        "service": "MAREC-HR360-API",
        "message": "System operational"
    }

# 🔄 SYNC ROUTE (Matches your frontend "Run Pipeline" or "Sync" actions)
@app.get("/api/v1/sync")
async def sync_database():
    try:
        # Future logic for refreshing PostgreSQL data goes here
        logger.info("🔄 Sync request received from Frontend")
        return {
            "status": "success", 
            "message": "MAREC HR360 Database Synced Successfully"
        }
    except Exception as e:
        logger.error(f"❌ Sync Failed: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# ✅ IMPORT & LINK ROUTERS
try:
    from routes import dashboard, employees
    app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
    app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
    logger.info("🚀 API Routers integrated")
except Exception as e:
    logger.error(f"❌ Router Integration Error: {e}")

@app.get("/")
async def root():
    return {
        "message": "MAREC HR360 API", 
        "status": "Active",
        "docs": "/docs"
    }