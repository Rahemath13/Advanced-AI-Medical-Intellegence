from pathlib import Path
from typing import Any

import requests


class APIClient:
    """Client for communicating with the FastAPI backend."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/health",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def analyze_image(
        self,
        image_path: str | Path,
    ) -> dict[str, Any]:
        path = Path(image_path)

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
                timeout=300,
            )

        response.raise_for_status()

        payload = response.json()

        if payload.get("status") != "success":
            raise RuntimeError(
                payload.get(
                    "message",
                    "Analysis failed.",
                )
            )

        return payload.get("data", payload)

    def get_history(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/predictions/history",
            params={"limit": limit},
            timeout=20,
        )

        response.raise_for_status()

        payload = response.json()

        if isinstance(payload, list):
            return payload

        return payload.get(
            "data",
            payload.get("items", []),
        )