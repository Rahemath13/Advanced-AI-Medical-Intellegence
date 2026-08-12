from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.repository import get_prediction, get_predictions

router = APIRouter(
    prefix="/predictions",
    tags=["Prediction History"],
)


@router.get("/history")
def prediction_history(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),  # noqa: B008
) -> dict:
    """Return prediction history, newest first."""

    records = get_predictions(
        db,
        limit=limit,
        offset=offset,
    )

    return {
        "status": "success",
        "count": len(records),
        "data": [
            {
                "id": record.id,
                "image_filename": record.image_filename,
                "predicted_class": record.predicted_class,
                "confidence": record.confidence,
                "model_version": record.model_version,
                "gradcam_path": record.gradcam_path,
                "status": record.status,
                "created_at": record.created_at.isoformat(),
            }
            for record in records
        ],
    }


@router.get("/history/{prediction_id}")
def prediction_detail(
    prediction_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> dict:
    """Return a single prediction including its generated report."""

    record = get_prediction(
        db,
        prediction_id,
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Prediction {prediction_id} not found.",
        )

    return {
        "status": "success",
        "data": {
            "id": record.id,
            "image_filename": record.image_filename,
            "image_path": record.image_path,
            "predicted_class": record.predicted_class,
            "confidence": record.confidence,
            "model_version": record.model_version,
            "gradcam_path": record.gradcam_path,
            "generated_report": record.generated_report,
            "status": record.status,
            "created_at": record.created_at.isoformat(),
        },
    }