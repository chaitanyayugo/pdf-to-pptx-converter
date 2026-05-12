from pydantic import BaseModel
from typing import Optional, Literal

class UploadResponse(BaseModel):
    job_id: str
    filename: str
    status: Literal["queued"] = "queued"

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int = 0
    message: Optional[str] = None
    result_file: Optional[str] = None
