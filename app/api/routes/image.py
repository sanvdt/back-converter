from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid
import redis
from rq import Queue
from app.services.image_to_pdf import convert_image_to_pdf
from fastapi.responses import FileResponse

router = APIRouter()

redis_conn = redis.Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

@router.post("/convert/image")
async def convert_image(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex
    input_dir = Path("storage/input")
    output_dir = Path("storage/output")
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = input_dir / f"{file_id}_{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = queue.enqueue(convert_image_to_pdf, str(input_path), str(output_dir))

    return {"job_id": job.get_id(), "status": job.get_status()}

@router.get("/convert/image/status/{job_id}")
def get_image_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Job não encontrado"}

    if job.is_finished:
        pdf_path = job.result
        if Path(pdf_path).exists():
            return FileResponse(path=pdf_path, filename=Path(pdf_path).name)
        else:
            return {"error": "Arquivo PDF não encontrado"}

    return {"job_id": job.get_id(), "status": job.get_status()}
