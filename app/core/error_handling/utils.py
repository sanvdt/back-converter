import hashlib
import re
from pathlib import Path

def sanitize_filename(path: Path, max_length=100) -> Path:
    safe_stem = re.sub(r"[^\w\-\.]", "_", path.stem)[:max_length]
    return path.parent / f"{safe_stem}{path.suffix}"
