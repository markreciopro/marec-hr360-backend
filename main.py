from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# ✅ SETUP LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MAREC HR360 API")

# 🌐 CORS CONFIG - Allows your GitHub/Local frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ IMPORT & LINK ROUTERS
try:
    from routes import dashboard, employees
    app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
    app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
    logger.info("🚀 All MAREC routes attached successfully")
except ImportError as e:
    logger.error(f"❌ Import Error: {e}. Check your __init__.py spelling!")

@app.get("/")
def root():
    return {"message": "MAREC HR360 API is Live", "owner": "MAREC Insights"}