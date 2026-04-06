from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    ML_CLIENT_ID = os.getenv("ML_CLIENT_ID", "")
    ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET", "")
    ML_REDIRECT_URI = os.getenv("ML_REDIRECT_URI", "")
    ML_AUTH_CODE = os.getenv("ML_AUTH_CODE", "")
    ML_ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN", "")
    ML_REFRESH_TOKEN = os.getenv("ML_REFRESH_TOKEN", "")
    ML_TOKEN_EXPIRES_AT = os.getenv("ML_TOKEN_EXPIRES_AT", "")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    VITE_API_URL = os.getenv("VITE_API_URL", "http://localhost:8000")

settings = Settings()