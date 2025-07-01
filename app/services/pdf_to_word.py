from pdf2docx import Converter
from pathlib import Path

def convert_pdf_to_word(input_path: str, output_dir: str) -> str:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_file = output_dir / (input_path.stem + ".docx")

    cv = Converter(str(input_path))
    cv.convert(str(output_file))
    cv.close()

    return str(output_file)
