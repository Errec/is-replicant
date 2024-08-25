"""Module for application configuration."""
from pydantic import Field  # Correct import for Field
from pydantic_settings import BaseSettings  # Correct import for BaseSettings

class Settings(BaseSettings):
    """Class for application settings."""
    PROJECT_NAME: str = "is-Replicant"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Pydantic configuration for the Settings class."""
        env_file = ".env"

settings = Settings()
