from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class PredictionHistory(Base):
    """
    Stores the complete history of medical image predictions.

    This table is designed to preserve the complete inference
    lifecycle: image -> prediction -> explanation -> report.
    """

    __tablename__ = "prediction_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    image_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    image_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    predicted_class: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    gradcam_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    generated_report: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="completed",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<PredictionHistory("
            f"id={self.id}, "
            f"class={self.predicted_class}, "
            f"confidence={self.confidence}"
            f")>"
        )
