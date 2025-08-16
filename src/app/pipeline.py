# src/app/pipeline.py

import os
from openai import OpenAI
from .pdf_loader import extract_text_from_pdf
from dotenv import load_dotenv

load_dotenv()  # loads .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))

def chunk_text(text, max_tokens=2000):
    """Split text into chunks that OpenAI can handle safely."""
    words = text.split()
    chunks, current_chunk = [], []
    current_len = 0

    for word in words:
        current_chunk.append(word)
        current_len += 1
        if current_len >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk, current_len = [], 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summarize_text(text: str) -> str:
    """Summarize text using OpenAI GPT model."""
    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # cheaper/faster model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n\n{chunk}"}
            ],
            temperature=0.3,
            max_tokens=400
        )
        summaries.append(response.choices[0].message.content.strip())

    # Final summary of all summaries
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": "Combine these summaries into a final concise summary:\n\n" + "\n\n".join(summaries)}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return final_response.choices[0].message.content.strip()

def summarize_pdf(pdf_path: str) -> str:
    text = extract_text_from_pdf(pdf_path)
    return summarize_text(text)
