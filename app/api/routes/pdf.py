from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import os
import redis
from rq import Queue
from app.services.pdf_to_word import convert_pdf_to_word

router = APIRouter()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
redis_conn = redis.from_url(redis_url)
queue = Queue(connection=redis_conn)

@router.post("/convert/pdf-to-word")
async def convert_pdf(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex
    input_dir = Path("storage/input")
    output_dir = Path("storage/output")
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = input_dir / f"{file_id}_{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = queue.enqueue(convert_pdf_to_word, str(input_path), str(output_dir))

    return {"job_id": job.get_id(), "status": job.get_status()}

@router.get("/convert/pdf-to-word/status/{job_id}")
def get_pdf_to_word_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Job não encontrado"}

    status = job.get_status()
    result = None

    if job.is_finished:
        docx_path = Path(job.result)
        if docx_path.exists():
            result = f"/download/{docx_path.name}"
        else:
            result = "Arquivo .docx não encontrado"

    return {
        "job_id": job.id,
        "status": status,
        "result": result
    }

@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = Path("storage/output") / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    return {"error": "Arquivo não encontrado"}, 404

