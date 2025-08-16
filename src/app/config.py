
from dataclasses import dataclass

@dataclass
class PipelineConfig:
    model_name: str = "t5-small"
    device: str = "cpu"  # or "cuda"
    max_chars: int = 3000  # per chunk
    overlap: int = 300     # characters overlap between chunks
    max_summary_tokens: int = 128  # per chunk
    final_summary_tokens: int = 160  # fuse step
