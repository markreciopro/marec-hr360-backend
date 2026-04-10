# routes/dashboard.py

from fastapi import APIRouter, HTTPException
import pandas as pd

from database import engine

router = APIRouter()


@router.get("/api/v1/employees")
def get_employees():

    try:
        df = pd.read_sql("SELECT * FROM employees", engine)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/summary")
def get_summary():
    """Optional: precomputed dashboard metrics"""

    try:
        df = pd.read_sql("SELECT * FROM employees", engine)

        if df.empty:
            return {"headcount": 0, "attrition": 0}

        headcount = len(df)

        terminated = df[
            df["status"].str.lower() == "terminated"
        ].shape[0]

        attrition = round((terminated / headcount) * 100, 2) if headcount else 0

        dept_counts = (
            df["department"]
            .value_counts()
            .to_dict()
        )

        return {
            "headcount": headcount,
            "attrition": attrition,
            "departments": dept_counts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))