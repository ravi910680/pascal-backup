# Pascal’s Academy — Book/PDF Summarization Pipeline

A compact, production-leaning implementation of a PDF ingestion and summarization pipeline — suitable as a starting point for a “Blinkist-like” product.

## What this does

- Accepts a PDF upload (CLI or API; you may also pass plain text for testing).
- Extracts and cleans text from the PDF.
- Chunks the text into model-friendly windows with light overlap.
- Summarizes each chunk with a local Hugging Face model (default `t5-small`), then fuses chunk summaries into a final abstract.
- Returns the final summary via CLI or a minimal FastAPI server.

> **Why this approach?**  
> It’s pragmatic: simple modules, clear boundaries, easily swappable models, and fast to run on a laptop. You can later upgrade the summarizer (e.g., to `facebook/bart-large-cnn`, `google/pegasus-xsum`, or an API-based LLM) without touching ingestion/cleaning/chunking logic.

## Quickstart

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> If you have a GPU, also install a CUDA-enabled PyTorch wheel from https://pytorch.org to speed up inference.

### 2) Run CLI on a PDF

```bash
python -m app.cli --pdf /path/to/book.pdf --model t5-small --max-chars 3000
```

Use a plain text file instead (for quick testing):

```bash
python -m app.cli --text-file sample_data/sample.txt --model t5-small
```

### 3) Run the API

```bash
uvicorn app.api:app --reload
```

Then POST a PDF or text to `http://127.0.0.1:8000/summarize`.

- `multipart/form-data` with field `file` (PDF) **or**
- JSON with `{ "text": "..." }`

### Notable Design Choices

- **Small, swappable summarizer**: default to `t5-small` for speed. Replace with a stronger model by flag or config.
- **Deterministic chunking**: character-based windows with overlap to preserve context across boundaries.
- **Two-stage summarization**: per-chunk summaries fused into a final abstract to avoid token limits.
- **Pure-Python ingestion**: uses `pypdf` for robustness (few native deps). You can swap to `pdfminer.six` if you prefer.
- **Tested components**: unit tests for the cleaner and chunker to show approach to verifiability.

### Tradeoffs / Future Work

- Improve layout-aware extraction (tables/figures, reading order) by adding `unstructured` or `pdfplumber`.
- Add language detection + multilingual models.
- Add caching (e.g., on chunk hashes) to skip re-summarizing unchanged content.
- Stream results for long docs; add trace IDs and observability (OpenTelemetry).
- RAG extension: index chunks into a vector store and expose a `/ask` endpoint to answer questions grounded in the PDF.

## Project Structure

```
pascals-academy-summarizer/
├─ src/app/
│  ├─ config.py          # Defaults and knobs
│  ├─ pdf_loader.py      # PDF → raw text
│  ├─ text_cleaner.py    # Normalize whitespace, remove junk
│  ├─ chunker.py         # Deterministic windows with overlap
│  ├─ summarizer.py      # HF summarization wrapper
│  ├─ pipeline.py        # Orchestration
│  ├─ cli.py             # Command-line entry point
│  └─ api.py             # FastAPI server
├─ tests/
│  ├─ test_chunker.py
│  └─ test_cleaner.py
├─ sample_data/
│  └─ sample.txt
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```

---

## Example

```
$ python -m app.cli --text-file sample_data/sample.txt --max-chars 1200
[INFO] Loaded 2,134 chars. Chunking into 2 piece(s).
[INFO] Summarizing with t5-small ...
[SUMMARY]
<your summary here>
```

