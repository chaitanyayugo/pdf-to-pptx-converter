import json
import uuid
from pathlib import Path

from rq import Worker, Queue, Connection
from redis import Redis

from .config import REDIS_URL, UPLOAD_DIR, OUTPUT_DIR
from .converter import convert_pdf_to_pptx

redis_conn = Redis.from_url(REDIS_URL)
queue = Queue("pdf_to_pptx", connection=redis_conn)


def process_job(input_file: str, job_id: str):
    result_path = convert_pdf_to_pptx(input_file, str(OUTPUT_DIR / f"{job_id}.pptx"))
    meta_path = OUTPUT_DIR / f"{job_id}.json"
    meta_path.write_text(json.dumps({"job_id": job_id, "status": "done", "result_file": result_path}))
    return result_path


if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker([queue])
        worker.work()
