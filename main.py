from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title="HR360 Backend API",
    description="FastAPI backend for HR360 with Supabase PostgreSQL",
    version="1.0.0"
)

# CORS (allows frontend + CodePen + local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check ---
@app.get("/")
def root():
    return {"status": "ok", "message": "HR360 backend running"}

# --- Database Test Endpoint ---
@app.get("/test-db")
def test_db(db: Session = get_db()):
    try:
        db.execute("SELECT 1;")
        return {"status": "ok", "message": "Connected to database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
