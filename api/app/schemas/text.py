from typing import List, Dict
from pydantic import BaseModel, confloat, constr

class TextAnalysisRequest(BaseModel):
    text: constr(min_length=1)

class WordFrequency(BaseModel):
    """Pydantic model for word frequency."""
    word: str
    frequency: int  # Frequency as a count

class WordAnalysis(BaseModel):
    """Pydantic model for word analysis."""
    total_word_count: int
    unique_word_count: int
    word_frequencies: List[WordFrequency]  # List of word-frequency pairs
    top_n_words: List[str]
    ai_likelihood: confloat(ge=0, le=1)  # AI likelihood should be between 0 and 1

class PhraseFrequency(BaseModel):
    """Pydantic model for phrase frequency."""
    phrase: str
    frequency: int  # Frequency as a count

class PhraseAnalysis(BaseModel):
    total_phrase_count: int
    matched_ai_phrases: List[PhraseFrequency]  # List of phrase-frequency pairs
    ai_likelihood: confloat(ge=0, le=1)

class TextAnalysisResponse(BaseModel):
    word_analysis: WordAnalysis
    phrase_analysis: PhraseAnalysis
    overall_ai_likelihood: confloat(ge=0, le=1)

class PhraseCreate(BaseModel):
    phrase: constr(min_length=1)
    ai_likelihood: confloat(ge=0, le=1)

class WordCreate(BaseModel):
    word: constr(min_length=1)
    ai_likelihood: confloat(ge=0, le=1)
