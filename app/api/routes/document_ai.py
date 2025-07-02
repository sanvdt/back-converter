from fastapi import APIRouter, UploadFile, File, Form
from app.services.document_ai import save_document, query_document

router = APIRouter()

@router.post("/document/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    doc_id = save_document(content, file.filename)
    return {"doc_id": doc_id, "message": "Documento salvo e processado."}

@router.post("/document/ask")
async def ask_about_document(doc_id: str = Form(...), question: str = Form(...)):
    answer = query_document(doc_id, question)
    return {"answer": answer}
