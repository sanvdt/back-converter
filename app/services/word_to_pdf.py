import subprocess
from pathlib import Path

def convert_word_to_pdf(input_path: str, output_dir: str) -> str:
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(input_path)
    ], check=True)

    return str(output_dir / (input_path.stem + ".pdf"))
