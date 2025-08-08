"""Utility functions for analyzing text and detecting AI-generated content.

The service provides basic natural language processing (NLP) features using
`nltk` for tokenization and leverages the database to look up known words and
phrases that are commonly produced by AI systems. Each helper is documented
with its purpose and expected inputs to make the implementation clear and
maintainable.
"""
import os
from collections import Counter
from typing import List

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sqlalchemy.orm import Session

from app.db import models
from app.schemas.text import (
    MatchedPhrase,
    PhraseAnalysis,
    TextAnalysisResponse,
    WordAnalysis,
)

# Set NLTK data path
nltk.data.path.append(os.environ.get("NLTK_DATA", "/app/nltk_data"))


def analyze_text(text: str, db: Session) -> TextAnalysisResponse:
    """Perform NLP analysis on ``text`` and compute AI-likelihood metrics.

    The function tokenizes the incoming text, gathers frequency statistics, and
    queries the database for previously observed AI-generated words and phrases.
    Results are aggregated into :class:`TextAnalysisResponse` which contains
    granular information about words and phrases as well as an overall
    likelihood score.

    Parameters
    ----------
    text:
        Text to analyse.
    db:
        SQLAlchemy session used for retrieving known words and phrases.
    """

    # Tokenize and normalise text. ``word_tokenize`` returns punctuation which
    # we filter out to avoid skewing statistics.
    words = [w for w in word_tokenize(text.lower()) if w.isalpha()]
    word_freq = Counter(words)

    # Retrieve known AI words/phrases from the database once for reuse.
    db_words = db.query(models.Word).all()
    db_phrases = db.query(models.Phrase).all()

    word_analysis = WordAnalysis(
        total_word_count=len(words),
        unique_word_count=len(set(words)),
        word_frequencies=[
            {"word": word, "frequency": freq / len(words)}
            for word, freq in word_freq.most_common(10)
        ],
        top_n_words=[word for word, _ in word_freq.most_common(5)],
        ai_likelihood=calculate_word_ai_likelihood(words, db_words),
    )

    phrase_analysis = PhraseAnalysis(
        total_phrase_count=len(sent_tokenize(text)),
        matched_ai_phrases=find_matched_phrases(text, db_phrases),
        ai_likelihood=calculate_phrase_ai_likelihood(text, db_phrases),
    )

    overall_ai_likelihood = (
        word_analysis.ai_likelihood + phrase_analysis.ai_likelihood
    ) / 2

    return TextAnalysisResponse(
        word_analysis=word_analysis,
        phrase_analysis=phrase_analysis,
        overall_ai_likelihood=overall_ai_likelihood,
    )


def calculate_word_ai_likelihood(
    words: List[str], db_words: List[models.Word]
) -> float:
    """Return the average AI likelihood for all ``words``.

    Parameters
    ----------
    words:
        Tokenised words extracted from the analysed text.
    db_words:
        List of :class:`~app.db.models.Word` instances fetched from the
        database.

    Returns
    -------
    float
        Average ``ai_likelihood`` of matched words, or ``0`` when no matches
        are found.
    """

    ai_words = [db_word for db_word in db_words if db_word.word in words]
    return (
        sum(word.ai_likelihood for word in ai_words) / len(ai_words)
        if ai_words
        else 0
    )


def find_matched_phrases(
    text: str, db_phrases: List[models.Phrase]
) -> List[MatchedPhrase]:
    """Find phrases from the database that occur within ``text``.

    Parameters
    ----------
    text:
        Raw text being analysed.
    db_phrases:
        List of :class:`~app.db.models.Phrase` instances available in the
        database.
    """

    return [
        MatchedPhrase(phrase=phrase.phrase, ai_likelihood=phrase.ai_likelihood)
        for phrase in db_phrases
        if phrase.phrase.lower() in text.lower()
    ]


def calculate_phrase_ai_likelihood(
    text: str, db_phrases: List[models.Phrase]
) -> float:
    """Return the average AI likelihood of phrases present in ``text``.

    Parameters
    ----------
    text:
        Raw text being analysed.
    db_phrases:
        List of :class:`~app.db.models.Phrase` instances fetched from the
        database.

    Returns
    -------
    float
        Average ``ai_likelihood`` of matched phrases, or ``0`` if no database
        phrases are found within the text.
    """

    matched_phrases = find_matched_phrases(text, db_phrases)
    return (
        sum(phrase.ai_likelihood for phrase in matched_phrases) / len(matched_phrases)
        if matched_phrases
        else 0
    )
