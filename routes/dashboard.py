from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    return {
        "workforce": 842,
        "attrition": 12,
        "timeToHire": 28
    }