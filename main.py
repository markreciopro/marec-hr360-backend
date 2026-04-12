from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os
from sqlalchemy import create_engine
from database import engine, Base

# =========================
# INIT APP (MUST BE FIRST)
# =========================
app = FastAPI(title="Marec HR360 API")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CREATE TABLES
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# ROOT
# =========================
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# =========================
# UPLOAD (HYBRID)
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    df = df.dropna()
    df.columns = [c.lower().strip() for c in df.columns]

    # SAVE LOCAL / PRIMARY
    df.to_sql("employees", engine, if_exists="replace", index=False)

    # OPTIONAL CLOUD SYNC
    if os.getenv("ENV") == "local" and os.getenv("CLOUD_DB_URL"):
        try:
            cloud_engine = create_engine(
                os.getenv("CLOUD_DB_URL"),
                connect_args={"sslmode": "require"}
            )
            df.to_sql("employees", cloud_engine, if_exists="replace", index=False)
            print("✅ Synced to cloud")
        except Exception as e:
            print("⚠️ Cloud sync failed:", e)

    return {"message": "Upload complete", "rows": len(df)}

@app.get("/")
def root():
    return {"message": "Marec HR360 API running"}

# =========================
# ANALYTICS
# =========================
@app.get("/analytics")
def get_analytics():

    df = pd.read_sql("SELECT * FROM employees", engine)

    if df.empty:
        return {"message": "No data"}

    headcount = len(df)
    terminated = len(df[df["status"] == "terminated"])
    attrition = (terminated / headcount) * 100

    avg_salary = df["salary"].mean()
    avg_tenure = df["tenure"].mean()

    return {
        "headcount": headcount,
        "attrition": round(attrition, 2),
        "avg_salary": round(avg_salary, 2),
        "avg_tenure": round(avg_tenure, 2),
        "data": df.to_dict(orient="records")
    }