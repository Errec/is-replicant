from sqlalchemy.orm import Session
from collections import Counter
import spacy
from app.db import models
from app.schemas.text import WordAnalysis, PhraseAnalysis

# Initialize the spaCy model
nlp = spacy.load("en_core_web_sm")

def calculate_word_ai_likelihood(words, db_words):
    """Calculate the likelihood that the text is AI-generated based on word analysis."""
    matched_words = [word for word in words if word in {w.word for w in db_words}]
    ai_likelihood = len(matched_words) / len(words) if words else 0
    return ai_likelihood

def calculate_phrase_ai_likelihood(text, db_phrases):
    """Calculate the likelihood that the text is AI-generated based on phrase analysis."""
    matched_phrases = [
        phrase.phrase for phrase in db_phrases if phrase.phrase in text
    ]
    ai_likelihood = len(matched_phrases) / len(db_phrases) if db_phrases else 0
    return ai_likelihood

def find_matched_phrases(text, db_phrases):
    """Find phrases in the text that match those in the database."""
    matched_phrases = [
        {"phrase": phrase.phrase, "frequency": text.count(phrase.phrase)}
        for phrase in db_phrases if phrase.phrase in text
    ]
    return matched_phrases

def analyze_text(text: str, db: Session):
    try:
        # Process the text using spaCy
        doc = nlp(text.lower())
        words = [token.text for token in doc]

        db_words = db.query(models.Word).all()
        db_phrases = db.query(models.Phrase).all()

        # Updated to ensure the dictionary format matches the Pydantic schema
        word_frequencies = [{"word": word, "frequency": freq} for word, freq in Counter(words).most_common()]

        word_analysis = WordAnalysis(
            total_word_count=len(words),
            unique_word_count=len(set(words)),
            word_frequencies=word_frequencies,
            top_n_words=[word for word, _ in Counter(words).most_common(10)],
            ai_likelihood=calculate_word_ai_likelihood(words, db_words),
        )

        phrase_analysis = PhraseAnalysis(
            total_phrase_count=len(db_phrases),
            matched_ai_phrases=find_matched_phrases(text, db_phrases),
            ai_likelihood=calculate_phrase_ai_likelihood(text, db_phrases),
        )

        overall_ai_likelihood = (
            word_analysis.ai_likelihood + phrase_analysis.ai_likelihood
        ) / 2

        return word_analysis, phrase_analysis, overall_ai_likelihood

    except Exception as e:
        raise Exception(f"An error occurred during analysis: {str(e)}") from e
