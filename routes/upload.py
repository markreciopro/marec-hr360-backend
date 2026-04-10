# routes/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from database import engine
from pipeline import process_file

router = APIRouter()


@router.post("/api/v1/run-pipeline")
async def run_pipeline(file: UploadFile = File(...)):

    try:
        # PROCESS
        df = process_file(file)

        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # SAVE TO POSTGRES
        df.to_sql("employees", engine, if_exists="replace", index=False)

        return {
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns)
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))