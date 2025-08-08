"""API endpoint for text analysis."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import get_db
from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.text_analysis import analyze_text

router = APIRouter()

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze(request: TextAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze the given text for AI-generated content.

    - **text**: The text to be analyzed

    Returns a detailed analysis of the text, including word analysis, phrase analysis,
    and overall AI likelihood.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty")

    try:
        return analyze_text(request.text, db)
    except SQLAlchemyError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail="Database error") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
