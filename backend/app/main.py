import json
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from rq.job import Job

from .config import CORS_ORIGINS, UPLOAD_DIR, OUTPUT_DIR, MAX_UPLOAD_SIZE_GB
from .models import UploadResponse, JobStatus
from .queue import queue, redis_conn
from .worker import process_job

app = FastAPI(title="PDF to PPTX Converter")

origins = [o.strip() for o in CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    job_id = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{job_id}.pdf"

    size = 0
    with input_path.open("wb") as f:
        while True:
            chunk = await file.read(1024 * 1024 * 8)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_UPLOAD_SIZE_GB * 1024 * 1024 * 1024:
                input_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="File too large")
            f.write(chunk)

    queue.enqueue(process_job, str(input_path), job_id, job_id=job_id)
    return UploadResponse(job_id=job_id, filename=file.filename)


@app.get("/status/{job_id}", response_model=JobStatus)
def status(job_id: str):
    meta_path = OUTPUT_DIR / f"{job_id}.json"
    if meta_path.exists():
        data = json.loads(meta_path.read_text())
        return JobStatus(
            job_id=job_id,
            status=data.get("status", "done"),
            progress=100,
            message="Completed",
            result_file=data.get("result_file"),
        )
    return JobStatus(job_id=job_id, status="queued", progress=0, message="Processing")


@app.get("/download/{job_id}")
def download(job_id: str):
    pptx_path = OUTPUT_DIR / f"{job_id}.pptx"
    if not pptx_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(pptx_path), filename=f"{job_id}.pptx")
