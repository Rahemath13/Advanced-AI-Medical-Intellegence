from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.repository import (
    create_prediction,
    get_prediction,
    get_predictions,
    update_prediction_report,
)


def create_test_database():
    """Create an isolated in-memory SQLite database for testing."""

    # Import models so SQLAlchemy registers the tables.
    from app.database import models  # noqa: F401

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return TestingSessionLocal


def test_create_prediction():
    TestingSessionLocal = create_test_database()

    with TestingSessionLocal() as db:
        prediction = create_prediction(
            db,
            image_filename="chest_xray_001.png",
            image_path="data/uploads/chest_xray_001.png",
            predicted_class="Pneumonia",
            confidence=0.94,
            model_version="efficientnet-b0-v1",
        )

        assert prediction.id is not None
        assert prediction.predicted_class == "Pneumonia"
        assert prediction.confidence == 0.94
        assert prediction.model_version == "efficientnet-b0-v1"


def test_get_prediction():
    TestingSessionLocal = create_test_database()

    with TestingSessionLocal() as db:
        created = create_prediction(
            db,
            image_filename="xray.png",
            image_path=None,
            predicted_class="Normal",
            confidence=0.91,
            model_version="test-model",
        )

        result = get_prediction(db, created.id)

        assert result is not None
        assert result.id == created.id
        assert result.predicted_class == "Normal"


def test_get_predictions():
    TestingSessionLocal = create_test_database()

    with TestingSessionLocal() as db:
        create_prediction(
            db,
            image_filename="xray1.png",
            image_path=None,
            predicted_class="Normal",
            confidence=0.90,
            model_version="test-model",
        )

        create_prediction(
            db,
            image_filename="xray2.png",
            image_path=None,
            predicted_class="Pneumonia",
            confidence=0.87,
            model_version="test-model",
        )

        results = get_predictions(db)

        assert len(results) == 2


def test_update_prediction_report():
    TestingSessionLocal = create_test_database()

    with TestingSessionLocal() as db:
        prediction = create_prediction(
            db,
            image_filename="xray.png",
            image_path=None,
            predicted_class="Pneumonia",
            confidence=0.95,
            model_version="test-model",
        )

        updated = update_prediction_report(
            db,
            prediction.id,
            "AI-assisted report generated.",
        )

        assert updated is not None
        assert updated.generated_report == "AI-assisted report generated."
