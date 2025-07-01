from pathlib import Path
from PIL import Image

def convert_image_to_pdf(input_path: str, output_dir: str) -> str:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(input_path).convert("RGB")
    output_path = output_dir / (input_path.stem + ".pdf")
    image.save(output_path, "PDF", resolution=100.0)

    return str(output_path)
