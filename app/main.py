from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import word
from app.api.routes import image
from app.api.routes import compress
from app.api.routes import pdf

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
