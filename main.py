# =========================
# 📦 IMPORTS
# =========================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# ✅ Import routers
from routes import dashboard
from routes import data_quality
from routes import pipeline


# =========================
# 🛠️ LOGGING CONFIG
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================
# 🚀 APP INIT
# =========================
app = FastAPI(
    title="MAREC HR360 API",
    description="Workforce Intelligence & Analytics Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# =========================
# 🌐 CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 Restrict this later to your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 🔗 ROUTERS (CORRECT ORDER)
# =========================
app.include_router(dashboard.router)
app.include_router(data_quality.router)
app.include_router(pipeline.router)


# =========================
# 🟢 STARTUP EVENT
# =========================
@app.on_event("startup")
def startup_event():
    logger.info("🚀 MAREC HR360 API is starting...")


# =========================
# 🔴 SHUTDOWN EVENT
# =========================
@app.on_event("shutdown")
def shutdown_event():
    logger.info("🛑 MAREC HR360 API is shutting down...")


# =========================
# 🏠 ROOT ENDPOINT
# =========================
@app.get("/")
def root():
    return {
        "message": "MAREC HR360 API running 🚀",
        "docs": "/docs",
        "health": "/health"
    }


# =========================
# ❤️ HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MAREC HR360 API",
        "version": "1.0.0"
    }