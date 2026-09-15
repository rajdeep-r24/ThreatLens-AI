from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import setup_initial_data
from app.api.v1.auth import router as auth_router
from app.api.v1.protected_routes import router as protected_router
from app.api.v1.files import router as files_router
from app.api.v1.predictions import router as predictions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and seed initial demo users + scans on startup
    setup_initial_data()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="ThreatLens-AI: Malware Classification & Threat Detection System API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers (Primary standard)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(protected_router, prefix=settings.API_V1_STR)
app.include_router(files_router, prefix=settings.API_V1_STR)
app.include_router(predictions_router, prefix=settings.API_V1_STR)

# Register aliases for frontend client compatibility (/api/...)
app.include_router(auth_router, prefix="/api")
app.include_router(files_router, prefix="/api")
app.include_router(predictions_router, prefix="/api")


@app.get("/", tags=["Health"])
def root():
    return {
        "name": settings.PROJECT_NAME,
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.get("/api/health", tags=["Health"])
def api_health_check():
    return {
        "status": "online",
        "system": "ThreatLens AI System Core",
        "milestone": 1,
        "database": "connected"
    }
