from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_stats():
    """Feeds the Top Cards in your dashboard"""
    return {
        "stats": [
            {"label": "Total Headcount", "value": "124", "trend": "+12%", "isPositive": True},
            {"label": "Active Recruits", "value": "45", "trend": "+5%", "isPositive": True},
            {"label": "Retention Rate", "value": "94.2%", "trend": "-0.5%", "isPositive": False},
            {"label": "Avg Time to Hire", "value": "18 Days", "trend": "-2 Days", "isPositive": True}
        ]
    }

@router.get("/budget")
async def get_budget():
    """Feeds the Departmental Budget Chart"""
    return [
        {"department": "Engineering", "budget": 150000, "spent": 132000},
        {"department": "Marketing", "budget": 85000, "spent": 72000},
        {"department": "Sales", "budget": 120000, "spent": 115000},
        {"department": "Operations", "budget": 95000, "spent": 88000}
    ]