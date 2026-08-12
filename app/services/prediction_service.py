from pathlib import Path

import torch
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.repository import create_prediction
from app.llm.groq_service import GroqMedicalReportService
from app.llm.schemas import MedicalReportRequest
from app.ml.xai import (
    create_overlay,
    generate_gradcam,
    load_xai_model,
    preprocess_image,
    save_gradcam,
)


class PredictionService:
    """End-to-end medical image prediction service."""

    def __init__(self) -> None:
        settings = get_settings()

        self.settings = settings

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.checkpoint = Path(settings.model_path)

        if not self.checkpoint.exists():
            raise FileNotFoundError(f"Model checkpoint not found: {self.checkpoint}")

        self.model = load_xai_model(
            self.checkpoint,
            self.device,
        )

        self.llm_service = GroqMedicalReportService()

    def analyze(
        self,
        image_path: str | Path,
        db: Session,
    ) -> dict:
        """
        Run complete medical image analysis.

        Pipeline:
        image -> deep learning prediction -> Grad-CAM
        -> LLM report -> database persistence.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        image, image_tensor = preprocess_image(image_path)

        grayscale_cam, predicted_class, probabilities = generate_gradcam(
            model=self.model,
            image_tensor=image_tensor,
            device=self.device,
        )

        prediction = "PNEUMONIA" if predicted_class == 1 else "NORMAL"

        normal_probability = float(probabilities[0])
        pneumonia_probability = float(probabilities[1])

        confidence = max(
            normal_probability,
            pneumonia_probability,
        )

        visualization = create_overlay(
            image,
            grayscale_cam,
        )

        xai_directory = Path("models/xai")
        xai_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        xai_path = xai_directory / f"{image_path.stem}_gradcam.jpg"

        save_gradcam(
            visualization,
            xai_path,
        )

        report_request = MedicalReportRequest(
            prediction=prediction,
            confidence=confidence,
            normal_probability=normal_probability,
            pneumonia_probability=pneumonia_probability,
        )

        report = self.llm_service.generate_report(
            image_path=image_path,
            request=report_request,
        )

        report_data = report.model_dump()

        prediction_record = create_prediction(
            db,
            image_filename=image_path.name,
            image_path=str(image_path),
            predicted_class=prediction,
            confidence=confidence,
            model_version=self.settings.app_version,
            gradcam_path=str(xai_path),
            generated_report=report.model_dump_json(),
            status="completed",
        )

        return {
            "prediction_id": prediction_record.id,
            "prediction": prediction,
            "confidence": confidence,
            "normal_probability": normal_probability,
            "pneumonia_probability": pneumonia_probability,
            "model_version": self.settings.app_version,
            "xai_path": str(xai_path),
            "report": report_data,
        }
