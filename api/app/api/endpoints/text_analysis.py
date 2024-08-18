from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.text_analysis import analyze_text

router = APIRouter()

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze(request: TextAnalysisRequest, db: Session = Depends(get_db)):
    return analyze_text(request.text, db)