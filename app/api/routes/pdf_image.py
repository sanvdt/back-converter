from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import redis
from rq import Queue
from app.services.pdf_to_image import convert_pdf_to_images
import os

router = APIRouter()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
redis_conn = redis.from_url(redis_url)
queue = Queue(connection=redis_conn)

@router.post("/convert/pdf-to-image")
async def convert_pdf_to_image(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex
    input_dir = Path("storage/input")
    output_dir = Path("storage/output")
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = input_dir / f"{file_id}_{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = queue.enqueue(convert_pdf_to_images, str(input_path), str(output_dir))

    return {"job_id": job.get_id(), "status": job.get_status()}

@router.get("/convert/pdf-to-image/status/{job_id}")
def get_pdf_to_image_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Job não encontrado"}

    status = job.get_status()
    result = None

    if job.is_finished:
        image_paths = job.result
        if image_paths and isinstance(image_paths, list) and all(Path(p).exists() for p in image_paths):
            result = f"/download/{Path(image_paths[0]).name}"
        else:
            result = "Imagens não encontradas"

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
