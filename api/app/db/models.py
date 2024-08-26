from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Phrase(Base):
    """Class representing phrases table in the database."""
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String(255), unique=True, index=True)  # Added a length constraint
    ai_likelihood = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('ai_likelihood >= 0 AND ai_likelihood <= 1', name='ai_likelihood_range'),
    )


class Word(Base):
    """Class representing words table in the database."""
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), unique=True, index=True)  # Added a length constraint
    ai_likelihood = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('ai_likelihood >= 0 AND ai_likelihood <= 1', name='ai_likelihood_range'),
    )
