import pandas as pd

STANDARD_SCHEMA = {
    "salary": ["salary", "pay", "income", "wage", "compensation"],
    "dept": ["dept", "department", "team", "division"],
    "tenure": ["tenure", "years", "service", "years_at_company"],
    "status": ["status", "employment", "state", "employment_status"]
}

def map_columns(df):
    mapped = {}

    for standard, variations in STANDARD_SCHEMA.items():
        for col in df.columns:
            if any(v in col.lower() for v in variations):
                mapped[standard] = col
                break

    return mapped


def normalize_schema(df):
    df.columns = df.columns.str.lower().str.strip()

    mapping = map_columns(df)

    std = pd.DataFrame()

    # SAFE extraction
    std["salary"] = pd.to_numeric(df.get(mapping.get("salary")), errors="coerce").fillna(0)
    std["dept"] = df.get(mapping.get("dept"), "Unknown").astype(str).fillna("Unknown")
    std["tenure"] = pd.to_numeric(df.get(mapping.get("tenure")), errors="coerce").fillna(0)
    std["status"] = df.get(mapping.get("status"), "active").astype(str).str.lower()

    std["client_id"] = "default"

    return std, mapping