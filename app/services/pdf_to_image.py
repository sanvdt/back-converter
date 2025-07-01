from pdf2image import convert_from_path
from pathlib import Path

def convert_pdf_to_images(input_path: str, output_dir: str) -> list[str]:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(str(input_path))

    image_paths = []
    for i, image in enumerate(images):
        image_path = output_dir / f"{input_path.stem}_page_{i + 1}.jpg"
        image.save(image_path, "JPEG")
        image_paths.append(str(image_path))

    return image_paths
