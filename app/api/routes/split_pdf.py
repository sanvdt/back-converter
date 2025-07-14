from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import json
import redis
from rq import Queue
from app.services.split_pdf import split_pdf
import os
redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
redis_conn = redis.from_url(redis_url)
queue = Queue(connection=redis_conn)

router = APIRouter()

@router.post("/convert/split-pdf")
async def split_pdf_route(
    file: UploadFile = File(...),
    pages: str = Form(default=None)
):
    """
    Recebe um PDF para separar.

    - Se pages for None ou vazio, separa todas as páginas individualmente.
    - Se pages for lista JSON, separa só essas páginas num único arquivo.

    Exemplo de pages: "[0,2,5]" para extrair páginas 1, 3 e 6 (0-index).
    """
    file_id = uuid.uuid4().hex
    input_dir = Path("storage/split_input")
    output_dir = Path("storage/split_output")
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = input_dir / f"{file_id}_{file.filename}"
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if pages:
        pages_list = json.loads(pages)
    else:
        pages_list = None

    job = queue.enqueue(split_pdf, str(input_path), str(output_dir), pages_list)

    return {"job_id": job.get_id(), "status": job.get_status()}


@router.get("/split/download/{filename}")
def download_file(filename: str):
    file_path = Path("storage/split_output") / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    return {"error": "Arquivo não encontrado"}, 404

@router.get("/convert/split-pdf/status/{job_id}")
def get_split_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Job não encontrado"}

    status = job.get_status()
    result = None

    if job.is_finished:
        output_files = job.result
        if output_files and isinstance(output_files, list) and all(Path(p).exists() for p in output_files):
            result = f"/split/download/{Path(output_files[0]).name}"
        else:
            result = "Arquivo(s) não encontrado(s)"

    return {
        "job_id": job.id,
        "status": status,
        "result": result
    }
