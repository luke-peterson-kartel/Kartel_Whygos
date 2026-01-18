"""
Main FastAPI Application

Entry point for the Kartel WhyGO Management API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# Import routers (we'll create these next)
from .routers import auth, users, onboarding, company, departments, individuals, outcomes


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    description="REST API for Kartel WhyGO Management System"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(company.router, prefix="/api/company", tags=["Company Goals"])
app.include_router(departments.router, prefix="/api/departments", tags=["Departments"])
app.include_router(individuals.router, prefix="/api/individuals", tags=["Individual Goals"])
app.include_router(outcomes.router, prefix="/api/outcomes", tags=["Outcomes & Progress"])


@app.get("/", tags=["Root"])
def root():
    """API root - returns basic info"""
    return {
        "message": "Kartel WhyGO Management API",
        "version": settings.version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.version
    }
