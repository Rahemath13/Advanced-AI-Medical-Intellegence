import json
from pathlib import Path

import torch

from app.ml.data_loader import create_dataloaders
from app.ml.evaluator import (
    evaluate_model,
    load_checkpoint,
)
from app.ml.training_config import TrainingConfig


def main() -> None:
    """Evaluate the best model on the untouched test set."""

    config = TrainingConfig()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _, _, test_loader = create_dataloaders(
        data_directory=config.data_directory,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
    )

    checkpoint_path = Path(config.checkpoint_directory) / config.best_model_name

    model = load_checkpoint(
        checkpoint_path,
        device,
    )

    print("=" * 60)
    print("INDEPENDENT TEST EVALUATION")
    print("=" * 60)
    print(f"Device: {device}")
    print(f"Test samples: {len(test_loader.dataset)}")
    print("=" * 60)

    metrics = evaluate_model(
        model=model,
        data_loader=test_loader,
        device=device,
    )

    print("\nMODEL PERFORMANCE")
    print("-" * 60)

    print(f"Accuracy    : {metrics['accuracy']:.4f}")

    print(f"Precision   : {metrics['precision']:.4f}")

    print(f"Recall      : {metrics['recall']:.4f}")

    print(f"Specificity : {metrics['specificity']:.4f}")

    print(f"F1 Score    : {metrics['f1_score']:.4f}")

    print(f"ROC-AUC     : {metrics['roc_auc']:.4f}")

    print("\nCONFUSION MATRIX")
    print("-" * 60)

    print("[[TN, FP],")
    print(" [FN, TP]]")

    print(f"[[{metrics['true_negative']}, {metrics['false_positive']}],")

    print(f" [{metrics['false_negative']}, {metrics['true_positive']}]]")

    print("\nCLASSIFICATION REPORT")
    print("-" * 60)

    print(metrics["classification_report"])

    output_directory = Path("models/evaluation")

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics_to_save = {
        key: value for key, value in metrics.items() if key != "classification_report"
    }

    metrics_to_save["classification_report"] = metrics["classification_report"]

    output_file = output_directory / "test_metrics.json"

    output_file.write_text(
        json.dumps(
            metrics_to_save,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\nMetrics saved to: {output_file}")


if __name__ == "__main__":
    main()
