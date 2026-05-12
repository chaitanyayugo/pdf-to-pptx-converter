from pathlib import Path
from app.config import UPLOAD_DIR, OUTPUT_DIR


def save_upload(job_id: str, data: bytes):
    path = UPLOAD_DIR / f"{job_id}.pdf"
    path.write_bytes(data)
    return path


def output_file(job_id: str):
    return OUTPUT_DIR / f"{job_id}.pptx"
