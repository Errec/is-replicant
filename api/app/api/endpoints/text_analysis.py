from fastapi import APIRouter, Depends, HTTPException
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

    Returns a detailed analysis of the text, including word analysis, phrase analysis,
    and overall AI likelihood.
    """
    try:
        word_analysis, phrase_analysis, overall_ai_likelihood = analyze_text(request.text, db)
        return TextAnalysisResponse(
            word_analysis=word_analysis,
            phrase_analysis=phrase_analysis,
            overall_ai_likelihood=overall_ai_likelihood,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during analysis: {str(e)}"
        ) from e
