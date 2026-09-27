from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI E-Commerce"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:56643@localhost:5432/fastapi"
    DEBUG: bool = True
    
    # JWT Authentication
    SECRET_KEY: str = "super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
