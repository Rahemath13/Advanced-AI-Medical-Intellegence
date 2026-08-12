from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    page_title: str = "AI Medical Intelligence Platform"
    page_icon: str = "🫁"
    api_url: str = "http://127.0.0.1:8000"
    max_upload_size_mb: int = 10


CONFIG = Config()