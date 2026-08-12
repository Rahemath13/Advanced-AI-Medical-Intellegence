from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import PredictionHistory


def create_prediction(
    db: Session,
    *,
    image_filename: str,
    image_path: str | None,
    predicted_class: str,
    confidence: float,
    model_version: str,
    gradcam_path: str | None = None,
    generated_report: str | None = None,
    status: str = "completed",
) -> PredictionHistory:
    """Create and persist a prediction history record."""

    prediction = PredictionHistory(
        image_filename=image_filename,
        image_path=image_path,
        predicted_class=predicted_class,
        confidence=confidence,
        model_version=model_version,
        gradcam_path=gradcam_path,
        generated_report=generated_report,
        status=status,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


def get_prediction(
    db: Session,
    prediction_id: int,
) -> PredictionHistory | None:
    """Retrieve a prediction by ID."""

    statement = select(PredictionHistory).where(PredictionHistory.id == prediction_id)

    return db.scalar(statement)


def get_predictions(
    db: Session,
    *,
    limit: int = 50,
    offset: int = 0,
) -> Sequence[PredictionHistory]:
    """Return prediction history ordered by newest first."""

    statement = (
        select(PredictionHistory)
        .order_by(PredictionHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()


def update_prediction_report(
    db: Session,
    prediction_id: int,
    report: str,
) -> PredictionHistory | None:
    """Update the generated medical report."""

    prediction = get_prediction(db, prediction_id)

    if prediction is None:
        return None

    prediction.generated_report = report
    db.commit()
    db.refresh(prediction)

    return prediction
