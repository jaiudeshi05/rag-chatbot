from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[4]

class Settings(BaseSettings):
    # ==========================================
    # APPLICATION
    # ==========================================
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool
    HOST: str
    PORT: int
    FRONTEND_URL: str = "http://localhost:3000"

    # ==========================================
    # JWT
    # ==========================================
    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_DAYS: int

    # ==========================================
    # GOOGLE OAUTH
    # ==========================================
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # ==========================================
    # DATABASE
    # ==========================================
    DATABASE_URL: str = ""

    # ==========================================
    # REDIS
    # ==========================================
    REDIS_URL: str

    # ==========================================
    # QDRANT
    # ==========================================
    QDRANT_URL: str

    # ==========================================
    # BACKBLAZE B2
    # ==========================================
    B2_BUCKET_NAME: str = ""
    B2_ENDPOINT: str = ""
    B2_ACCESS_KEY: str = ""
    B2_SECRET_KEY: str = ""
    B2_REGION: str = ""

    # ==========================================
    # HUGGING FACE
    # ==========================================
    HF_API_KEY: str = ""
    HF_BGE_ENDPOINT: str = ""

    # ==========================================
    # NVIDIA
    # ==========================================
    NVIDIA_API_KEY: str = ""
    NVIDIA_QWEN_ENDPOINT: str = ""
    NVIDIA_QWEN_VL_ENDPOINT: str = ""

    # ==========================================
    # RAG
    # ==========================================
    DEFAULT_TOP_K: int
    DEFAULT_CHUNK_SIZE: int
    DEFAULT_CHUNK_OVERLAP: int

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value: bool | str) -> bool:
        if isinstance(value, bool):
            return value

        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on", "debug", "development"}:
            return True
        if normalized in {"0", "false", "no", "off", "release", "production"}:
            return False

        return value


settings = Settings()
