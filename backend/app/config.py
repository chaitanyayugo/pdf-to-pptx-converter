import os
from pathlib import Path

APP_NAME = os.getenv("APP_NAME", "pdf-to-pptx")
ENV = os.getenv("ENV", "development")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/data/uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/data/outputs"))
MAX_UPLOAD_SIZE_GB = int(os.getenv("MAX_UPLOAD_SIZE_GB", "1"))
ENABLE_OCR = os.getenv("ENABLE_OCR", "true").lower() == "true"
OCR_LANG = os.getenv("OCR_LANG", "en")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
