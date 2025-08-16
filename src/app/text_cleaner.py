
import re

# Basic text normalization suitable for summarization
def clean_text(text: str) -> str:
    if not text:
        return ""
    # Normalize line breaks & spaces
    text = text.replace("\u00A0", " ")
    text = re.sub(r"[\t\r]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)  # collapse multiple blank lines
    text = re.sub(r"\s{2,}", " ", text)          # collapse excessive spaces
    # Remove common artifacts
    text = re.sub(r"—\s*", "—", text)
    # Trim
    return text.strip()
