from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from torch.utils.data import DataLoader

from app.ml.model import create_model

CLASS_NAMES = [
    "NORMAL",
    "PNEUMONIA",
]


def load_checkpoint(
    checkpoint_path: str | Path,
    device: torch.device,
):
    """Load the trained model checkpoint."""

    checkpoint_path = Path(checkpoint_path)

    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    model = create_model(
        pretrained=False,
    )

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=False,
    )

    model.load_state_dict(checkpoint["model_state_dict"])

    model.to(device)
    model.eval()

    return model


def evaluate_model(
    model,
    data_loader: DataLoader,
    device: torch.device,
) -> dict:
    """Evaluate the model on an independent dataset."""

    all_targets: list[int] = []
    all_predictions: list[int] = []
    all_probabilities: list[float] = []

    model.eval()

    with torch.no_grad():
        for images, targets in data_loader:
            images = images.to(device)

            outputs = model(images)

            probabilities = torch.softmax(
                outputs,
                dim=1,
            )

            predictions = probabilities.argmax(dim=1)

            all_targets.extend(targets.numpy().tolist())

            all_predictions.extend(predictions.cpu().numpy().tolist())

            pneumonia_probabilities = probabilities[:, 1].cpu().numpy().tolist()

            all_probabilities.extend(pneumonia_probabilities)

    targets_array = np.asarray(all_targets)

    predictions_array = np.asarray(all_predictions)

    probabilities_array = np.asarray(all_probabilities)

    accuracy = accuracy_score(
        targets_array,
        predictions_array,
    )

    precision = precision_score(
        targets_array,
        predictions_array,
        zero_division=0,
    )

    recall = recall_score(
        targets_array,
        predictions_array,
        zero_division=0,
    )

    f1 = f1_score(
        targets_array,
        predictions_array,
        zero_division=0,
    )

    try:
        roc_auc = roc_auc_score(
            targets_array,
            probabilities_array,
        )
    except ValueError:
        roc_auc = float("nan")

    matrix = confusion_matrix(
        targets_array,
        predictions_array,
        labels=[0, 1],
    )

    true_negative = matrix[0, 0]
    false_positive = matrix[0, 1]
    false_negative = matrix[1, 0]
    true_positive = matrix[1, 1]

    specificity = (
        true_negative / (true_negative + false_positive)
        if (true_negative + false_positive) > 0
        else 0.0
    )

    report = classification_report(
        targets_array,
        predictions_array,
        target_names=CLASS_NAMES,
        zero_division=0,
    )

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "specificity": float(specificity),
        "f1_score": float(f1),
        "roc_auc": float(roc_auc),
        "true_negative": int(true_negative),
        "false_positive": int(false_positive),
        "false_negative": int(false_negative),
        "true_positive": int(true_positive),
        "classification_report": report,
    }
