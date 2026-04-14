from ai_engine import generate_insights
from risk_model import add_risk_scores
from ml_model import predict_risk
import pandas as pd


def compute_analytics(df):
    # =========================
    # EMPTY CHECK
    # =========================
    if df is None or df.empty:
        return {"message": "No data yet"}

    df = df.copy()

    # =========================
    # 🤖 ML RISK MODEL (PRIMARY)
    # =========================
    try:
        df = predict_risk(df)
        print("🤖 ML risk model applied")
    except Exception as e:
        print("⚠️ ML model failed, fallback:", e)

        try:
            df = add_risk_scores(df)
        except Exception as e2:
            print("❌ Risk fallback failed:", e2)

    # =========================
    # 🧠 DATA ENRICHMENT LAYER (NEW 🔥)
    # =========================
    try:
        # Salary segmentation
        if "salary" in df.columns:
            df["salary"] = pd.to_numeric(df["salary"], errors="coerce").fillna(0)

            df["salary_band"] = pd.cut(
                df["salary"],
                bins=[0, 40000, 70000, 100000, 200000, 9999999],
                labels=["Low", "Mid", "High", "Senior", "Executive"]
            )

        # Tenure segmentation
        if "tenure" in df.columns:
            df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").fillna(0)

            df["tenure_band"] = pd.cut(
                df["tenure"],
                bins=[0, 1, 3, 5, 10, 50],
                labels=["0-1", "1-3", "3-5", "5-10", "10+"]
            )

        # Department cleanup (fix undefined)
        if "dept" in df.columns:
            df["dept"] = df["dept"].fillna("Unknown").astype(str)

    except Exception as e:
        print("⚠️ Enrichment error:", e)

    # =========================
    # CORE METRICS
    # =========================
    headcount = len(df)

    # Attrition
    if "status" in df.columns:
        terminated = len(df[df["status"] == "terminated"])
        attrition = (terminated / headcount) * 100
    else:
        attrition = 0

    # Averages
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

    # ML probability
    avg_risk_prob = (
        round(df["risk_probability"].mean(), 3)
        if "risk_probability" in df.columns else None
    )

    # =========================
    # 📊 DISTRIBUTIONS (FOR CHARTS)
    # =========================
    try:
        dept_dist = (
            df["dept"].value_counts().to_dict()
            if "dept" in df.columns else {}
        )

        salary_dist = (
            df["salary_band"].value_counts().to_dict()
            if "salary_band" in df.columns else {}
        )

        tenure_dist = (
            df["tenure_band"].value_counts().to_dict()
            if "tenure_band" in df.columns else {}
        )

    except Exception as e:
        print("⚠️ Distribution error:", e)
        dept_dist = salary_dist = tenure_dist = {}

    # =========================
    # BUILD RESPONSE
    # =========================
    analytics = {
        "headcount": headcount,
        "attrition": round(attrition, 2),
        "avg_salary": round(avg_salary, 2),
        "avg_tenure": round(avg_tenure, 2),

        # 🔥 Risk metrics
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,

        # 🔥 ML signal
        "avg_risk_probability": avg_risk_prob,

        # 🔥 Chart-ready data
        "dept_distribution": dept_dist,
        "salary_distribution": salary_dist,
        "tenure_distribution": tenure_dist,

        # 🔥 Full dataset
        "data": df.to_dict(orient="records")
    }

    # =========================
    # 🤖 AI INSIGHTS ENGINE
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