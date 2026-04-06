from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

# DATABASE IMPORTS
try:
    from database import engine
    import models
    # Creates tables in PostgreSQL automatically
    models.Base.metadata.create_all(bind=engine)
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
# This allows your GitHub Pages site to securely talk to this Render API
origins = [
    "https://markreciopro.github.io",  # Your Live Site
    "http://127.0.0.1:8000",           # Local Testing
    "http://localhost:8000",           # Local Testing
    "http://localhost:5500",           # Live Server Extension
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛡️ GLOBAL ERROR LOGGING MIDDLEWARE
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"RID: {request.scope.get('root_path')} | Method: {request.method} | Path: {request.url.path} | Time: {formatted_process_time}ms")
        return response
    except Exception as e:
        logger.error(f"❌ Server Error on {request.url.path}: {str(e)}")
        raise e

# ✅ HEALTH CHECK ROUTE (Required for the Diagnostic Tool)
@app.get("/api/v1/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "timestamp": time.time(),
        "version": "1.0.0",
        "service": "MAREC-HR360-API"
    }

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
        "environment": "Production",
        "documentation": "/docs"
    }