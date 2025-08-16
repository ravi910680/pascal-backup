
from typing import List
from transformers import pipeline

class Summarizer:
    def __init__(self, model_name: str = "t5-small", device: str = "cpu"):
        # device: "cpu" or "cuda"
        device_idx = 0 if device == "cuda" else -1
        self.pipe = pipeline("summarization", model=model_name, device=device_idx)

    def summarize_chunks(self, chunks: List[str], max_tokens: int = 128) -> List[str]:
        # transformers pipeline uses 'max_length' and 'min_length' in tokens
        outputs = []
        for ch in chunks:
            # Guardrail: skip tiny chunks
            if len(ch.strip()) < 100:
                outputs.append(ch.strip())
                continue
            res = self.pipe(ch, max_length=max_tokens, min_length=max(30, max_tokens//3), do_sample=False)
            outputs.append(res[0]["summary_text"])
        return outputs

    def fuse(self, summaries: List[str], max_tokens: int = 160) -> str:
        text = "\n".join(summaries)
        res = self.pipe(text, max_length=max_tokens, min_length=max(40, max_tokens//3), do_sample=False)
        return res[0]["summary_text"]
