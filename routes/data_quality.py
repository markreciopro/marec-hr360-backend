from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter(prefix="/api/data-quality")

# =========================
# SUMMARY
# =========================
@router.post("/summary")
async def summary(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    result = {}
    for col in df.columns:
        result[col] = {
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique()),
            "mean": float(df[col].mean()) if pd.api.types.is_numeric_dtype(df[col]) else None,
            "min": str(df[col].min()),
            "max": str(df[col].max())
        }

    return result

# =========================
# CLEAN
# =========================
@router.post("/clean")
async def clean(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    df = df.drop_duplicates()
    df = df.fillna(0)

    return {"rows": len(df)}

# =========================
# ANALYZE
# =========================
@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    return {
        "missing_values": df.isnull().sum().to_dict()
    }

# =========================
# VALIDATE
# =========================
@router.post("/validate")
async def validate(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    return {
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "columns": list(df.columns)
    }