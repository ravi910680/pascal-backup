
from app.text_cleaner import clean_text

def test_clean_basic():
    raw = "Hello\n\n\nWorld\t\t!"
    cleaned = clean_text(raw)
    assert "World !" in cleaned or "World!" in cleaned
