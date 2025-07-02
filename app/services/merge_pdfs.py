from PyPDF2 import PdfMerger
from pathlib import Path

def merge_pdfs(pdf_paths: list[str], output_path: str) -> str:
    merger = PdfMerger()

    for pdf in pdf_paths:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()

    return output_path
