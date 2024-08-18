from fastapi import FastAPI
from app.api.endpoints import text_analysis, admin
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(text_analysis.router, prefix="/api/v1", tags=["text_analysis"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to the is-Replicant API"}