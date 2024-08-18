from pydantic import BaseModel
from typing import List, Dict

class TextAnalysisRequest(BaseModel):
    text: str

class WordAnalysis(BaseModel):
    total_word_count: int
    unique_word_count: int
    word_frequencies: List[Dict[str, float]]
    top_n_words: List[str]
    ai_likelihood: float

class PhraseAnalysis(BaseModel):
    total_phrase_count: int
    matched_ai_phrases: List[Dict[str, float]]
    ai_likelihood: float

class TextAnalysisResponse(BaseModel):
    word_analysis: WordAnalysis
    phrase_analysis: PhraseAnalysis
    overall_ai_likelihood: float

class PhraseCreate(BaseModel):
    phrase: str
    ai_likelihood: float

class WordCreate(BaseModel):
    word: str
    ai_likelihood: float