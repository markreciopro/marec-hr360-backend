from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_employees():
    return [
        {"id": 1, "name": "Mark Anthony Recio", "role": "Full Stack Dev", "status": "Active"},
        {"id": 2, "name": "Ken Arancibia", "role": "CEO", "status": "Active"},
        {"id": 3, "name": "Saurabh Dixit", "role": "Technical Recruiter", "status": "Active"}
    ]