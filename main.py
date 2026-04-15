from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd

from db.database import SessionLocal, get_db
from engine.engine import clean_data, transform_data, compute_analytics

app = FastAPI(
    title="HR360 Backend API",
    description="FastAPI backend for HR360 with Supabase PostgreSQL",
    version="1.0.0"
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def root():
    return {"status": "ok", "message": "HR360 backend running"}

# =========================
# DATABASE TEST ENDPOINT
# =========================
@app.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1;")
        return {"status": "ok", "message": "Connected to database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =========================
# FILE UPLOAD + INGESTION
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read Excel/CSV
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)

        # Clean + transform
        df = clean_data(df)
        std = transform_data(df)

        # Compute analytics
        analytics = compute_analytics(std)

        return {
            "status": "success",
            "rows": len(std),
            "analytics": analytics
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# =========================
# DASHBOARD ENDPOINT
# =========================
@app.get("/dashboard")
def dashboard():
    return {"message": "Dashboard endpoint placeholder — ready for DB integration"}
