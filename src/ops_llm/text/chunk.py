from pathlib import Path
from typing import Dict, Iterable
import re

# naive text splitter with overlap
def split_text(text: str, target_tokens: int = 600, overlap_tokens: int = 80) -> Iterable[str]:
    # crude token estimate: whitespace words
    words = text.split()
    step = max(target_tokens - overlap_tokens, 50)
    for i in range(0, len(words), step):
        yield ' '.join(words[i:i+target_tokens])

# trivial extractor for docx/pdf/txt will be added later
def extract_text_from_path(path: Path) -> str:
    return path.read_text(errors='ignore') if path.suffix.lower() == '.txt' else ''
