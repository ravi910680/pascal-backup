# Pascal’s Academy — Book/PDF Summarization Pipeline (OpenAI Edition)

A compact, production-leaning implementation of a PDF ingestion and summarization pipeline — powered by **OpenAI GPT models**. Suitable as a starting point for a “Blinkist-like” product.

## What this does

- Accepts a PDF upload (CLI or API; you may also pass plain text for testing).
- Extracts and cleans text from the PDF.
- Chunks the text into model-friendly windows with light overlap.
- Summarizes each chunk using the **OpenAI API**, then fuses chunk summaries into a final abstract.
- Returns the final summary via CLI or a minimal FastAPI server.

> **Why this approach?**  
> It’s pragmatic: simple modules, clear boundaries, easily swappable models, and scalable via OpenAI. You can later swap back to Hugging Face or any other provider without changing ingestion/cleaning/chunking logic.

---

## Quickstart

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# PDF Summarizer

Summarize PDF or text files using OpenAI GPT.

---

### 2) Set your OpenAI API key

Create a `.env` file in the project root with your API key:

```env
OPENAI_API_KEY=your_api_key_here

### 3) Test

python -m app.cli --pdf sample_data/test.pdf --max-chars 3000
