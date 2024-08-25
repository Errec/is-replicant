"""This module contains the dependencies for the API endpoints."""
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

def get_db():
    """Get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    """Get the current admin user from the token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token has expired using timezone-aware datetime objects
        token_exp = datetime.fromtimestamp(payload.get("exp", 0), tz=timezone.utc)
        if token_exp < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return payload  # Returning payload instead of just True

    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        ) from exc
