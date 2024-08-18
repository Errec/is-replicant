from fastapi import FastAPI
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

app.include_router(text_analysis.router, prefix="/api/v1", tags=["text_analysis"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the is-Replicant API"}