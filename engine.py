import pandas as pd

# =========================
# COLUMN DETECTION
# =========================
COLUMN_MAP = {
    "salary": ["salary", "pay", "income", "wage"],
    "department": ["dept", "department", "team"],
    "tenure": ["tenure", "years", "service"],
    "status": ["status", "employment", "state"],
    "employee_id": ["id", "employee_id", "emp_id"]
}

def detect_column(df, target):
    for col in df.columns:
        for keyword in COLUMN_MAP[target]:
            if keyword in col.lower():
                return col
    return None


# =========================
# CLEAN DATA
# =========================
def clean_data(df):
    df.columns = df.columns.str.strip().str.lower()

    # Fill missing
    df = df.fillna(0)

    # Remove duplicates
    df = df.drop_duplicates()

    return df


# =========================
# TRANSFORM TO STANDARD MODEL
# =========================
def transform_data(df):
    mapped = {}

    for key in COLUMN_MAP:
        col = detect_column(df, key)
        mapped[key] = col

    # Build standardized dataset
    std = pd.DataFrame()

    if mapped["salary"]:
        std["salary"] = pd.to_numeric(df[mapped["salary"]], errors="coerce").fillna(0)

    if mapped["department"]:
        std["dept"] = df[mapped["department"]].astype(str)

    if mapped["tenure"]:
        std["tenure"] = pd.to_numeric(df[mapped["tenure"]], errors="coerce").fillna(0)

    if mapped["status"]:
        std["status"] = df[mapped["status"]].astype(str).str.lower()

    return std


# =========================
# ANALYTICS ENGINE
# =========================
def compute_analytics(df):
    if df.empty:
        return {"message": "No data yet"}

    headcount = len(df)

    # Attrition
    if "status" in df.columns:
        attrition = (df["status"] == "terminated").sum() / headcount * 100
    else:
        attrition = 0

    avg_salary = df["salary"].mean() if "salary" in df.columns else 0
    avg_tenure = df["tenure"].mean() if "tenure" in df.columns else 0

    # Risk model (simple)
    high_risk = int(attrition > 15)

    return {
        "headcount": headcount,
        "attrition": round(attrition, 2),
        "avg_salary": round(avg_salary, 2),
        "avg_tenure": round(avg_tenure, 2),
        "high_risk": high_risk,
        "data": df.to_dict(orient="records")
    }