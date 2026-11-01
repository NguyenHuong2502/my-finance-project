from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.database.connection import test_connection

app = FastAPI(
    title="MyFinance API",
    description="Personal Finance Management System",
    version="1.0.0"
)
app.include_router(auth_router)

# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to MyFinance API"
    }


# Backend Health Check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Database Health Check
@app.get("/health/database")
def database_health_check():
    database_name = test_connection()

    return {
        "status": "connected",
        "database": database_name
    }