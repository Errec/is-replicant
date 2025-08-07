"""Module for defining Pydantic models for text analysis API endpoints."""
from typing import List
from pydantic import BaseModel, confloat, constr


class WordFrequency(BaseModel):
    """Frequency information for a single word."""
    word: str
    frequency: confloat(ge=0, le=1)  # Frequency as a fraction between 0 and 1


class MatchedPhrase(BaseModel):
    """Representation of a phrase matched in the analysed text."""
    phrase: str
    ai_likelihood: confloat(ge=0, le=1)

class TextAnalysisRequest(BaseModel):
    """Pydantic model for the request body of the text analysis endpoint."""
    text: constr(min_length=1)  # Ensure that the text is not empty

class WordAnalysis(BaseModel):
    """Pydantic model for word analysis."""
    total_word_count: int
    unique_word_count: int
    word_frequencies: List[WordFrequency]
    top_n_words: List[str]
    ai_likelihood: confloat(ge=0, le=1)  # AI likelihood should be between 0 and 1

class PhraseAnalysis(BaseModel):
    """Pydantic model for phrase analysis."""
    total_phrase_count: int
    matched_ai_phrases: List[MatchedPhrase]
    ai_likelihood: confloat(ge=0, le=1)  # AI likelihood should be between 0 and 1

class TextAnalysisResponse(BaseModel):
    """Pydantic model for text analysis response."""
    word_analysis: WordAnalysis
    phrase_analysis: PhraseAnalysis
    overall_ai_likelihood: confloat(ge=0, le=1)  # AI likelihood should be between 0 and 1

class PhraseCreate(BaseModel):
    """Model for creating a new phrase."""
    phrase: constr(min_length=1)  # Ensure that the phrase is not empty
    ai_likelihood: confloat(ge=0, le=1)  # AI likelihood should be between 0 and 1

class WordCreate(BaseModel):
    """Model for creating a new word."""
    word: constr(min_length=1)  # Ensure that the word is not empty
    ai_likelihood: confloat(ge=0, le=1)  # AI likelihood should be between 0 and 1
