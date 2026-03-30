from fastapi import FastAPI
from routes import dashboard

app = FastAPI(title="MAREC HR360 API")

app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "MAREC HR360 API running"}