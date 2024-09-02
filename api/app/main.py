from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import text_analysis, admin
import traceback
import spacy

app = FastAPI(
    title="is-Replicant API",
    description="API for detecting AI-generated text",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_analysis.router, prefix="/api/v1", tags=["text_analysis"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": str(exc),
            "traceback": traceback.format_exc()
        },
    )

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the is-Replicant API"}

@app.on_event("startup")
async def startup_event():
    try:
        nlp = spacy.load("en_core_web_sm")
        print("spaCy model 'en_core_web_sm' loaded successfully")
    except Exception as e:
        print(f"Failed to load spaCy model. Error: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down the application...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
