import hashlib
import re
from pathlib import Path

def sanitize_filename(path: Path, max_length=100) -> Path:
    """Gera um nome de arquivo mais curto e seguro."""
    safe_stem = re.sub(r"[^\w\-\.]", "_", path.stem)[:max_length]
    hash_suffix = hashlib.md5(str(path).encode()).hexdigest()[:8]
    return path.parent / f"{hash_suffix}_{safe_stem}{path.suffix}"
