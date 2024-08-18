from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, unique=True, index=True)
    ai_likelihood = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True)
    ai_likelihood = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())