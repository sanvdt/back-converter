import subprocess
from pathlib import Path

def compress_pdf(input_path: str, output_dir: str, quality: str = "screen") -> str:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / (input_path.stem + "_compressed.pdf")

    quality_settings = ["/screen", "/ebook", "/printer", "/prepress"]
    if quality not in quality_settings:
        quality = "/screen"

    subprocess.run([
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        str(input_path)
    ], check=True)

    return str(output_path)
