from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(
    input_pdf_path: str, 
    output_dir: str, 
    pages_to_extract: list[int] | None = None
) -> list[str]:
    """
    Separa páginas do PDF.

    - input_pdf_path: caminho do PDF original
    - output_dir: pasta onde serão salvos os PDFs separados
    - pages_to_extract: lista de páginas (0-indexadas) a extrair. 
      Se None, extrai todas separadamente.

    Retorna lista de caminhos dos PDFs separados.
    """
    input_pdf_path = Path(input_pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(input_pdf_path))
    num_pages = len(reader.pages)
    output_files = []

    if pages_to_extract is None:
        for i in range(num_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            output_path = output_dir / f"{input_pdf_path.stem}_page_{i+1}.pdf"
            with open(output_path, "wb") as f_out:
                writer.write(f_out)
            output_files.append(str(output_path))
    else:
        writer = PdfWriter()
        for page_index in pages_to_extract:
            if 0 <= page_index < num_pages:
                writer.add_page(reader.pages[page_index])
            else:
                raise ValueError(f"Página inválida: {page_index + 1}")

        output_path = output_dir / f"{input_pdf_path.stem}_split.pdf"
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
        output_files.append(str(output_path))

    return output_files
