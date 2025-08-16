
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from .config import PipelineConfig
from .pipeline import summarize_pdf, summarize_text

app = FastAPI(title="Pascal's Academy Summarizer", version="0.1.0")

class TextIn(BaseModel):
    text: str
    model: str | None = "t5-small"
    device: str | None = "cpu"

@app.post("/summarize")
async def summarize_endpoint(file: UploadFile | None = File(default=None), text_in: TextIn | None = None):
    # Accept either a PDF in 'file' or JSON with 'text'
    model_name = "t5-small"
    device = "cpu"
    if text_in:
        if text_in.model:
            model_name = text_in.model
        if text_in.device:
            device = text_in.device

    cfg = PipelineConfig(model_name=model_name, device=device)

    if file is not None:
        tmp_path = f"/tmp/{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())
        summary = summarize_pdf(tmp_path, cfg)
        return {"summary": summary, "source": file.filename, "model": model_name}
    elif text_in is not None and text_in.text:
        summary = summarize_text(text_in.text, cfg)
        return {"summary": summary, "source": "raw_text", "model": model_name}
    else:
        return {"error": "Provide either a PDF file or JSON with 'text'."}
