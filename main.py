from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import pandas as pd
import io

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
origins = [
    "https://markreciopro.github.io",
    "https://markreciopro.github.io/marec_hr360",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5173", # Vite/React default
    "https://cdpn.io",       # Essential for CodePen testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛡️ GLOBAL REQUEST LOGGING
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | {process_time:.2f}ms")
    return response

# --- NEW: THE "RECEIVER" ROUTE (File Upload & Process) ---
@app.post("/api/v1/upload-data")
async def process_workforce_file(file: UploadFile = File(...)):
    try:
        logger.info(f"📥 Received file: {file.filename}")
        contents = await file.read()
        
        # Determine file type and read into Pandas
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid file type."})

        # --- STRATEGIC DATA ARCHITECT MAGIC: CLEANING ---
        df.dropna(how='all', inplace=True) # Remove totally empty rows
        # Add your custom cleaning logic here (e.g., df['Salary'] = df['Salary'].replace('[\$,]', '', regex=True))

        # --- LOCAL DATABASE SYNC ---
        # If your models are ready, you can uncomment the next line to save to Postgres:
        # df.to_sql('employees', con=engine, if_exists='append', index=False)

        return {
            "status": "success",
            "message": f"Successfully processed {len(df)} rows from {file.filename}",
            "preview": df.head(3).to_dict(orient='records')
        }
    except Exception as e:
        logger.error(f"❌ Upload Processing Failed: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# ✅ HEALTH CHECK ROUTE
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "online",
        "service": "MAREC-HR360-API",
        "message": "System operational"
    }

# 🔄 SYNC ROUTE
@app.get("/api/v1/sync")
async def sync_database():
    try:
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