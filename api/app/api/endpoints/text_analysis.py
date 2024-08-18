from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.text_analysis import analyze_text

router = APIRouter()

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze(request: TextAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze the given text for AI-generated content.

    - **text**: The text to be analyzed
    - **text_type**: The type of the text (e.g., "article", "cover letter", etc.)

    Returns a detailed analysis of the text, including word analysis, phrase analysis, and overall AI likelihood.
    """
    return analyze_text(request.text, db)