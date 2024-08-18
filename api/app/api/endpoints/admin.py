from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_admin
from app.schemas.text import PhraseCreate, WordCreate
from app.db import models

router = APIRouter()

@router.post("/phrases", dependencies=[Depends(get_current_admin)])
async def create_phrase(phrase: PhraseCreate, db: Session = Depends(get_db)):
    db_phrase = models.Phrase(**phrase.dict())
    db.add(db_phrase)
    db.commit()
    db.refresh(db_phrase)
    return db_phrase

@router.post("/words", dependencies=[Depends(get_current_admin)])
async def create_word(word: WordCreate, db: Session = Depends(get_db)):
    db_word = models.Word(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

# Add more CRUD operations (update, delete, get) for words and phrases here