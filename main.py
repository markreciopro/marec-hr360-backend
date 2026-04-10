from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from sqlalchemy import create_engine

app = FastAPI()

# ===============================
# DATABASE CONNECTION
# ===============================
DATABASE_URL = "postgresql://postgres:password@localhost:5432/marec_db"
engine = create_engine(DATABASE_URL)

# ===============================
# CORS (Frontend Connection)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# ROOT
# ===============================
@app.get("/")
def root():
    return {"message": "MAREC HR360 API running"}

# ===============================
# RUN PIPELINE (UPLOAD + CLEAN + STORE)
# ===============================
@app.post("/api/v1/run-pipeline")
async def run_pipeline(file: UploadFile = File(...)):

    try:
        # ======================
        # LOAD FILE
        # ======================
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # ======================
        # CLEAN DATA
        # ======================
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

        if "department" not in df.columns:
            df["department"] = "Unknown"
        else:
            df["department"] = df["department"].fillna("Unknown")

        if "status" not in df.columns:
            df["status"] = "Active"
        else:
            df["status"] = df["status"].astype(str).str.strip().str.title()

        # Remove empty rows
        df = df.dropna(how="all")

        if df.empty:
            raise HTTPException(status_code=400, detail="File contains no usable data")

        # ======================
        # SAVE TO POSTGRESQL
        # ======================
        df.to_sql("employees", engine, if_exists="replace", index=False)

        return {
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# FETCH DATA (DB → DASHBOARD)
# ===============================
@app.get("/api/v1/employees")
def get_employees():

    try:
        df = pd.read_sql("SELECT * FROM employees", engine)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# SUMMARY (OPTIONAL KPI ENDPOINT)
# ===============================
@app.get("/api/v1/summary")
def get_summary():

    try:
        df = pd.read_sql("SELECT * FROM employees", engine)

        if df.empty:
            return {"headcount": 0, "attrition": 0, "departments": {}}

        headcount = len(df)

        terminated = df[
            df["status"].str.lower() == "terminated"
        ].shape[0]

        attrition = round((terminated / headcount) * 100, 2) if headcount else 0

        dept_counts = df["department"].value_counts().to_dict()

        return {
            "headcount": headcount,
            "attrition": attrition,
            "departments": dept_counts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))