from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import word
from app.api.routes import image
from app.api.routes import compress
from app.api.routes import pdf
from app.api.routes import pdf_image
from app.api.routes import merge_pdf
from app.api.routes import split_pdf
from app.api.routes import document_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(word.router)
app.include_router(image.router)
app.include_router(compress.router)
app.include_router(pdf.router)
app.include_router(pdf_image.router)
app.include_router(merge_pdf.router)
app.include_router(split_pdf.router)
app.include_router(document_ai.router)