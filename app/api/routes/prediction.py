from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.prediction_service import PredictionService

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post("/analyze")
async def analyze_prediction(
    file: UploadFile = File(...),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> dict:
    """Analyze an uploaded medical image and save the result."""

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=("Unsupported image format. Use JPG, JPEG, PNG, or WEBP."),
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty.",
        )

    upload_directory = Path("data/uploads")
    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_filename = Path(file.filename or "uploaded_image").name

    image_path = upload_directory / safe_filename
    image_path.write_bytes(contents)

    try:
        service = PredictionService()

        result = service.analyze(
            image_path=image_path,
            db=db,
        )

        return {
            "status": "success",
            "message": "Medical image analyzed successfully.",
            "data": result,
        }

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        ) from exc
