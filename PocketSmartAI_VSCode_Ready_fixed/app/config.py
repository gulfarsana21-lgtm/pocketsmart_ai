import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME", "PocketSmart AI")
    APP_ENV = os.getenv("APP_ENV", "development")
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "replace-this-with-a-long-random-secret",
    )
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "pocketsmart.db"),
    )
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS = [
        item.strip()
        for item in os.getenv(
            "CORS_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000",
        ).split(",")
        if item.strip()
    ]
    UPLOAD_DIR = BASE_DIR / "uploads"


settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
