
from typing import List

def chunk_text(text: str, max_chars: int = 3000, overlap: int = 300) -> List[str]:
    if not text:
        return []
    if max_chars <= 0:
        return [text]
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= n:
            break
        start = max(0, end - overlap)
    return chunks
