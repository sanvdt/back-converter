from fastapi import APIRouter, UploadFile, File
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import redis
from rq import Queue
from app.core.error_handling.utils import sanitize_filename
from app.services.compress_pdf import compress_pdf

router = APIRouter()

redis_conn = redis.Redis(host='localhost', port=6379)
queue = Queue(connection=redis_conn)


@router.post("/compress/pdf")
async def compress(file: UploadFile = File(...)):
    prefix = "cuid_compress_pdf"
    file_id = uuid.uuid4().hex
    input_dir = Path("storage/input")
    output_dir = Path("storage/output")
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = sanitize_filename(Path(file.filename))
    new_filename = f"{prefix}_{file_id}_{safe_name.name}"
    input_path = input_dir / new_filename

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = queue.enqueue(compress_pdf, str(input_path), str(output_dir), "screen")

    return {"job_id": job.get_id(), "status": job.get_status()}


@router.get("/compress/status/{job_id}")
def get_compress_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Tarefa não encontrada"}

    if job.is_failed:
        error_msg = "Ocorreu um erro ao comprimir o PDF. O nome do arquivo pode ser muito longo. Tente novamente com um nome de arquivo mais curto."
        return {"job_id": job.get_id(), "status": "failed", "error": error_msg}

    if job.is_finished:
        pdf_path = job.result
        if Path(pdf_path).exists():
            return FileResponse(path=pdf_path, filename=Path(pdf_path).name)
        else:
            return {"error": "Arquivo PDF comprimido não encontrado"}

    return {"job_id": job.get_id(), "status": job.get_status()}