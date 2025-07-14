from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import redis
import json
from rq import Queue
from app.services.merge_pdfs import merge_pdfs
import os
redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
redis_conn = redis.from_url(redis_url)
queue = Queue(connection=redis_conn)

router = APIRouter()


@router.post("/convert/merge-pdf")
async def merge_pdf(
    files: list[UploadFile] = File(...),
    ordem: str = Form(...)
):
    ordem = json.loads(ordem)
    file_id = uuid.uuid4().hex
    input_dir = Path("storage/merge_input") / file_id
    output_dir = Path("storage/merge_output")
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_paths = []

    for i, file in enumerate(files):
        file_path = input_dir / f"{i}_{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        input_paths.append(str(file_path))

    ordered_paths = [input_paths[i] for i in ordem]

    output_pdf_path = output_dir / f"{file_id}_merged.pdf"
    job = queue.enqueue('app.services.merge_pdfs.merge_pdfs', ordered_paths, str(output_pdf_path))

    return {"job_id": job.get_id(), "status": job.get_status()}


@router.get("/merge/download/{filename}")
def download_file(filename: str):
    file_path = Path("storage/merge_output") / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    return {"error": "Arquivo não encontrado"}, 404

@router.get("/convert/merge-pdf/status/{job_id}")
def get_merge_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Job não encontrado"}

    status = job.get_status()
    result = None

    if job.is_finished:
        merged_pdf = job.result
        if Path(merged_pdf).exists():
            result = f"/merge/download/{Path(merged_pdf).name}"
        else:
            result = "Arquivo mesclado não encontrado"

    return {
        "job_id": job.id,
        "status": status,
        "result": result
    }
