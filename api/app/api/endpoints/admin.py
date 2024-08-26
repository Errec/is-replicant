"""Admin API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.dependencies import get_db, get_current_admin
from app.schemas.text import PhraseCreate, WordCreate
from app.db import models

router = APIRouter()

@router.post("/phrases", dependencies=[Depends(get_current_admin)], status_code=status.HTTP_201_CREATED)
async def create_phrase(phrase: PhraseCreate, db: Session = Depends(get_db)):
    """Create a new phrase in the database."""
    try:
        db_phrase = models.Phrase(**phrase.dict())
        db.add(db_phrase)
        db.commit()
        db.refresh(db_phrase)
        return db_phrase
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Phrase already exists")

@router.post("/words", dependencies=[Depends(get_current_admin)], status_code=status.HTTP_201_CREATED)
async def create_word(word: WordCreate, db: Session = Depends(get_db)):
    """Create a new word in the database."""
    try:
        db_word = models.Word(**word.dict())
        db.add(db_word)
        db.commit()
        db.refresh(db_word)
        return db_word
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Word already exists")

@router.get("/phrases/{phrase_id}", response_model=PhraseCreate)
async def get_phrase(phrase_id: int, db: Session = Depends(get_db)):
    """Get a phrase by its ID."""
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()
    if not db_phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    return db_phrase

@router.get("/words/{word_id}", response_model=WordCreate)
async def get_word(word_id: int, db: Session = Depends(get_db)):
    """Get a word by its ID."""
    db_word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    return db_word

@router.put("/phrases/{phrase_id}", response_model=PhraseCreate)
async def update_phrase(phrase_id: int, phrase: PhraseCreate, db: Session = Depends(get_db)):
    """Update an existing phrase."""
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()
    if not db_phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    for key, value in phrase.dict().items():
        setattr(db_phrase, key, value)
    db.commit()
    db.refresh(db_phrase)
    return db_phrase

@router.put("/words/{word_id}", response_model=WordCreate)
async def update_word(word_id: int, word: WordCreate, db: Session = Depends(get_db)):
    """Update an existing word."""
    db_word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    for key, value in word.dict().items():
        setattr(db_word, key, value)
    db.commit()
    db.refresh(db_word)
    return db_word

@router.delete("/phrases/{phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    """Delete a phrase by its ID."""
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()
    if not db_phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    db.delete(db_phrase)
    db.commit()
    return

@router.delete("/words/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(word_id: int, db: Session = Depends(get_db)):
    """Delete a word by its ID."""
    db_word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    db.delete(db_word)
    db.commit()
    return
