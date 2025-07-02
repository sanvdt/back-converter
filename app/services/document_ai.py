import os
import uuid
from openai import OpenAI
from pathlib import Path
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

documents_db = {}

def extract_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8")
    else:
        raise ValueError("Formato não suportado")

def save_document(file: bytes, filename: str) -> str:
    ext = Path(filename).suffix
    temp_path = Path("storage/document_ai") / f"{uuid.uuid4()}{ext}"
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_bytes(file)

    text = extract_text(temp_path)
    temp_path.unlink()
    doc_id = str(uuid.uuid4())
    documents_db[doc_id] = text
    return doc_id

def query_document(doc_id: str, question: str) -> str:
    if doc_id not in documents_db:
        return "Documento não encontrado."

    context = documents_db[doc_id][:2000]
    prompt = f"Contexto:\n{context}\n\nPergunta: {question}\nResposta objetiva:"

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base no conteúdo de um documento."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=256
    )

    return response.choices[0].message.content.strip()
