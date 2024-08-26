from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import text_analysis, admin
from app.core.config import settings

app = FastAPI(
    title="is-Replicant API",
    description="API for detecting AI-generated text",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# CORS middleware (if required, customize origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_analysis.router, prefix="/api/v1", tags=["text_analysis"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/", tags=["root"])
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the is-Replicant API"}
