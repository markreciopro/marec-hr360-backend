from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router
from routes import dashboard

# =========================
# 🚀 APP INITIALIZATION
# =========================

app = FastAPI(
    title="MAREC HR360 API",
    description="Workforce Intelligence Platform API for HR Analytics, Recruiting, and AI Insights",
    version="1.0.0"
)

# =========================
# 🔐 CORS CONFIG (VERY IMPORTANT)
# =========================
# Allows your frontend (GitHub Pages / CodePen / local) to connect

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 Change to specific domain later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔌 ROUTES
# =========================

app.include_router(
    dashboard.router,
    tags=["MAREC HR360 Core APIs"]
)

# =========================
# 🏠 ROOT ENDPOINT
# =========================

@app.get("/")
def root():
    return {
        "message": "MAREC HR360 API running",
        "status": "active",
        "version": "1.0.0"
    }

# =========================
# ❤️ HEALTH CHECK (PRODUCTION READY)
# =========================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MAREC HR360 API"
    }