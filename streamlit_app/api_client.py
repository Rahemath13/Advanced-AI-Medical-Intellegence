from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Bootstrap project root into sys.path for Streamlit Cloud deployment
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests


class APIClient:
    """Client for communicating with the FastAPI backend with automatic in-process fallback."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=3,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {
                "status": "healthy",
                "application": "Advanced AI Medical Intelligence Platform",
                "version": "1.0.0",
                "environment": "standalone_streamlit",
            }

    def analyze_image(
        self,
        image_path: str | Path,
    ) -> dict[str, Any]:
        path = Path(image_path)

        try:
            with path.open("rb") as image_file:
                response = requests.post(
                    f"{self.base_url}/predictions/analyze",
                    files={
                        "file": (
                            path.name,
                            image_file,
                            "image/jpeg",
                        )
                    },
                    timeout=30,
                )
            if response.status_code == 200:
                payload = response.json()
                if payload.get("status") == "success":
                    return payload.get("data", payload)
        except Exception:
            pass

        # In-process Fallback for Streamlit Cloud deployment
        from app.services.prediction_service import PredictionService

        service = PredictionService()
        return service.analyze(path)

    def get_history(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        try:
            response = requests.get(
                f"{self.base_url}/predictions/history",
                params={"limit": limit},
                timeout=5,
            )
            if response.status_code == 200:
                payload = response.json()
                if isinstance(payload, list):
                    return payload
                if isinstance(payload, dict) and "data" in payload:
                    return payload["data"]
        except Exception:
            pass

        # In-process Fallback to SQLite Repository for Streamlit Cloud deployment
        try:
            from app.database.database import SessionLocal, init_db
            from app.database.repository import get_predictions

            init_db()
            db = SessionLocal()
            try:
                records = get_predictions(db, limit=limit)
                return [
                    {
                        "id": r.id,
                        "image_filename": r.image_filename,
                        "predicted_class": r.predicted_class,
                        "confidence": r.confidence,
                        "created_at": str(r.created_at),
                        "xai_image_path": r.xai_image_path,
                    }
                    for r in records
                ]
            finally:
                db.close()
        except Exception:
            return []