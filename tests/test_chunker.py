
from app.chunker import chunk_text

def test_chunking_overlap():
    text = "A" * 1000
    chunks = chunk_text(text, max_chars=300, overlap=50)
    assert chunks, "No chunks produced"
    # ensure overlap by checking adjacent boundaries
    if len(chunks) > 1:
        assert chunks[0][-50:] == chunks[1][:50]
