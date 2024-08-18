from sqlalchemy.orm import Session
from app.db import models
from app.schemas.text import TextAnalysisResponse, WordAnalysis, PhraseAnalysis
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')

def analyze_text(text: str, db: Session) -> TextAnalysisResponse:
    words = word_tokenize(text.lower())
    word_freq = Counter(words)
    
    db_words = db.query(models.Word).all()
    db_phrases = db.query(models.Phrase).all()
    
    word_analysis = WordAnalysis(
        total_word_count=len(words),
        unique_word_count=len(set(words)),
        word_frequencies=[{"word": word, "frequency": freq/len(words)} for word, freq in word_freq.most_common(10)],
        top_n_words=[word for word, _ in word_freq.most_common(5)],
        ai_likelihood=calculate_word_ai_likelihood(words, db_words)
    )
    
    phrase_analysis = PhraseAnalysis(
        total_phrase_count=len(text.split('.')),
        matched_ai_phrases=find_matched_phrases(text, db_phrases),
        ai_likelihood=calculate_phrase_ai_likelihood(text, db_phrases)
    )
    
    overall_ai_likelihood = (word_analysis.ai_likelihood + phrase_analysis.ai_likelihood) / 2
    
    return TextAnalysisResponse(
        word_analysis=word_analysis,
        phrase_analysis=phrase_analysis,
        overall_ai_likelihood=overall_ai_likelihood
    )

def calculate_word_ai_likelihood(words, db_words):
    ai_words = [db_word for db_word in db_words if db_word.word in words]
    return sum(word.ai_likelihood for word in ai_words) / len(ai_words) if ai_words else 0

def find_matched_phrases(text, db_phrases):
    return [{"phrase": phrase.phrase, "ai_likelihood": phrase.ai_likelihood} 
            for phrase in db_phrases if phrase.phrase.lower() in text.lower()]

def calculate_phrase_ai_likelihood(text, db_phrases):
    matched_phrases = find_matched_phrases(text, db_phrases)
    return sum(phrase['ai_likelihood'] for phrase in matched_phrases) / len(matched_phrases) if matched_phrases else 0