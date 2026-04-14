from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os

from database import engine, Base, save_data, load_data, sync_to_cloud
from ai_engine import generate_insights
from risk_model import add_risk_scores
from ml_model import predict_risk, train_and_save

# 🆕 NEW ENGINES
from schema_engine import normalize_schema
from validation_engine import validate_data

# =========================
# INIT APP
# =========================
app = FastAPI(
    title="Marec HR360 API",
    description="Enterprise AI HR Intelligence Platform",
    version="4.0"
)

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
# STARTUP
# =========================
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("🚀 Marec HR360 Enterprise API started")


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "Marec HR360 Enterprise API running 🚀"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


# =========================
# ENTERPRISE INGESTION PIPELINE
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files supported")

        contents = await file.read()

        # =========================
        # LOAD (robust encoding)
        # =========================
        try:
            df_raw = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        except:
            df_raw = pd.read_csv(io.StringIO(contents.decode("latin-1")))

        # =========================
        # CLEAN
        # =========================
        df_raw.columns = df_raw.columns.str.lower().str.strip()
        df_raw = df_raw.drop_duplicates()

        # =========================
        # 🧠 NORMALIZE (UNIVERSAL)
        # =========================
        df, mapping = normalize_schema(df_raw)

        if df.empty:
            raise HTTPException(status_code=400, detail="No usable HR data detected")

        # =========================
        # 🛡️ VALIDATION
        # =========================
        errors = validate_data(df)
        if errors:
            return {
                "status": "validation_warning",
                "errors": errors,
                "rows": len(df)
            }

        # =========================
        # 💾 SAVE (LOCAL)
        # =========================
        save_data(df)

        # =========================
        # ☁️ CLOUD SYNC
        # =========================
        if os.getenv("ENV") == "local":
            sync_to_cloud(df)

        # =========================
        # 🤖 AUTO RETRAIN MODEL
        # =========================
        try:
            train_and_save(df)
        except Exception as e:
            print("⚠️ Retrain skipped:", e)

        return {
            "status": "success",
            "rows_processed": len(df),
            "detected_schema": mapping
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# =========================
# ANALYTICS ENGINE (ENTERPRISE)
# =========================
def compute_analytics(df):
    if df is None or df.empty:
        return {"message": "No data yet"}

    df = df.copy()

    # =========================
    # 🤖 ML PREDICTION
    # =========================
    try:
        df = predict_risk(df)
    except Exception as e:
        print("⚠️ ML fallback:", e)
        try:
            df = add_risk_scores(df)
        except:
            pass

    headcount = len(df)

    # =========================
    # ATTRITION
    # =========================
    if "status" in df.columns:
        terminated = len(df[df["status"] == "terminated"])
        attrition = (terminated / headcount) * 100
    else:
        attrition = 0

    # =========================
    # METRICS
    # =========================
    avg_salary = df["salary"].mean() if "salary" in df.columns else 0
    avg_tenure = df["tenure"].mean() if "tenure" in df.columns else 0

    # =========================
    # RISK DISTRIBUTION
    # =========================
    if "risk_level" in df.columns:
        high_risk = len(df[df["risk_level"] == "HIGH"])
        medium_risk = len(df[df["risk_level"] == "MEDIUM"])
        low_risk = len(df[df["risk_level"] == "LOW"])
    else:
        high_risk = medium_risk = low_risk = 0

    avg_prob = (
        round(df["risk_probability"].mean(), 3)
        if "risk_probability" in df.columns else None
    )

    # =========================
    # 📊 ENRICHMENT (NEW)
    # =========================
    if "salary" in df.columns:
        df["salary_band"] = pd.cut(
            df["salary"],
            bins=[0, 40000, 70000, 100000, 200000],
            labels=["Low", "Mid", "High", "Exec"]
        )

    if "tenure" in df.columns:
        df["tenure_band"] = pd.cut(
            df["tenure"],
            bins=[0, 1, 3, 5, 10, 50],
            labels=["0-1", "1-3", "3-5", "5-10", "10+"]
        )

    analytics = {
        "headcount": headcount,
        "attrition": round(attrition, 2),
        "avg_salary": round(avg_salary, 2),
        "avg_tenure": round(avg_tenure, 2),

        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,

        "avg_risk_probability": avg_prob,

        "data": df.to_dict(orient="records")
    }

    # =========================
    # 🤖 AI INSIGHTS
    # =========================
    try:
        ai = generate_insights(df, analytics)
        analytics["ai_insights"] = ai.get("insights", [])
        analytics["recommendations"] = ai.get("recommendations", [])
    except Exception as e:
        print("⚠️ AI error:", e)
        analytics["ai_insights"] = []
        analytics["recommendations"] = []

    return analytics


# =========================
# ENDPOINTS
# =========================
@app.get("/analytics")
def get_analytics():
    df = load_data()
    return compute_analytics(df)


@app.get("/dashboard")
def dashboard():
    df = load_data()
    return compute_analytics(df)


@app.post("/retrain")
def retrain_model():
    try:
        df = load_data()

        if df.empty:
            return {"message": "No data available for training"}

        model, features = train_and_save(df)

        return {
            "status": "Model retrained",
            "features_used": features
        }

    except Exception as e:
        return {"error": str(e)}