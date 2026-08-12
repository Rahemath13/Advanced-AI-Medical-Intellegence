import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader

from app.ml.model import create_model
from app.ml.training_config import TrainingConfig


def set_seed(seed: int) -> None:
    """Set random seeds for reproducible training."""

    random.seed(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device(device_name: str = "auto") -> torch.device:
    """Select the training device."""

    if device_name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    return torch.device(device_name)


def calculate_class_weights(
    dataset: object,
    num_classes: int = 2,
) -> torch.Tensor:
    """Calculate inverse-frequency class weights."""

    if hasattr(dataset, "indices") and hasattr(dataset, "dataset"):
        base_dataset = dataset.dataset
        indices = dataset.indices

        labels = [base_dataset.samples[index][1] for index in indices]
    elif hasattr(dataset, "samples"):
        labels = [label for _, label in dataset.samples]
    else:
        raise TypeError(
            "Dataset must provide either 'samples' or 'indices' and 'dataset'."
        )

    counts = np.bincount(
        labels,
        minlength=num_classes,
    )

    if np.any(counts == 0):
        raise ValueError("Every class must contain at least one image.")

    total = counts.sum()

    weights = total / (num_classes * counts)

    return torch.tensor(
        weights,
        dtype=torch.float32,
    )
    labels = [label for _, label in dataset.samples]

    counts = np.bincount(
        labels,
        minlength=num_classes,
    )

    if np.any(counts == 0):
        raise ValueError("Every class must contain at least one image.")

    total = counts.sum()

    weights = total / (num_classes * counts)

    return torch.tensor(
        weights,
        dtype=torch.float32,
    )


def calculate_accuracy(
    outputs: torch.Tensor,
    targets: torch.Tensor,
) -> float:
    """Calculate classification accuracy."""

    predictions = outputs.argmax(dim=1)

    correct = (predictions == targets).sum().item()

    return correct / targets.size(0)


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: AdamW | None,
    device: torch.device,
) -> tuple[float, float]:
    """Run one training or validation epoch."""

    is_training = optimizer is not None

    if is_training:
        model.train()
    else:
        model.eval()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    context = torch.enable_grad() if is_training else torch.no_grad()

    with context:
        for images, targets in loader:
            images = images.to(device)
            targets = targets.to(device)

            if is_training:
                optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(
                outputs,
                targets,
            )

            if is_training:
                loss.backward()
                optimizer.step()

            batch_size = targets.size(0)

            total_loss += loss.item() * batch_size

            predictions = outputs.argmax(dim=1)

            total_correct += (predictions == targets).sum().item()

            total_samples += batch_size

    if total_samples == 0:
        raise ValueError("DataLoader contains no samples.")

    average_loss = total_loss / total_samples

    accuracy = total_correct / total_samples

    return average_loss, accuracy


def train_model(
    train_loader: DataLoader,
    validation_loader: DataLoader,
    config: TrainingConfig | None = None,
) -> dict[str, list[float]]:
    """Train EfficientNet-B0 and save the best checkpoint."""

    if config is None:
        config = TrainingConfig()

    set_seed(config.random_seed)

    device = get_device(config.device)

    print("=" * 60)
    print("MODEL TRAINING")
    print("=" * 60)
    print(f"Device: {device}")
    print(f"Epochs: {config.epochs}")
    print(f"Batch size: {config.batch_size}")
    print(f"Learning rate: {config.learning_rate}")
    print("=" * 60)

    model = create_model(
        pretrained=True,
    )

    model.to(device)

    class_weights = calculate_class_weights(train_loader.dataset).to(device)

    print(
        "Class weights:",
        class_weights.detach().cpu().tolist(),
    )

    criterion = nn.CrossEntropyLoss(
        weight=class_weights,
    )

    optimizer = AdamW(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )

    scheduler = ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=2,
    )

    checkpoint_directory = Path(config.checkpoint_directory)

    checkpoint_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    checkpoint_path = checkpoint_directory / config.best_model_name

    history: dict[str, list[float]] = {
        "train_loss": [],
        "train_accuracy": [],
        "validation_loss": [],
        "validation_accuracy": [],
    }

    best_validation_loss = float("inf")
    epochs_without_improvement = 0

    for epoch in range(1, config.epochs + 1):
        train_loss, train_accuracy = run_epoch(
            model=model,
            loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )

        validation_loss, validation_accuracy = run_epoch(
            model=model,
            loader=validation_loader,
            criterion=criterion,
            optimizer=None,
            device=device,
        )

        scheduler.step(validation_loss)

        history["train_loss"].append(train_loss)

        history["train_accuracy"].append(train_accuracy)

        history["validation_loss"].append(validation_loss)

        history["validation_accuracy"].append(validation_accuracy)

        current_lr = optimizer.param_groups[0]["lr"]

        print(
            f"Epoch {epoch:02d}/{config.epochs} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Train Acc: {train_accuracy:.4f} | "
            f"Val Loss: {validation_loss:.4f} | "
            f"Val Acc: {validation_accuracy:.4f} | "
            f"LR: {current_lr:.2e}"
        )

        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            epochs_without_improvement = 0

            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "validation_loss": validation_loss,
                    "validation_accuracy": validation_accuracy,
                    "epoch": epoch,
                    "class_names": [
                        "NORMAL",
                        "PNEUMONIA",
                    ],
                },
                checkpoint_path,
            )

            print(f"  ✓ Best checkpoint saved: {checkpoint_path}")

        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= config.patience:
            print(f"Early stopping after epoch {epoch}.")
            break

    history_path = checkpoint_directory / "training_history.json"

    history_path.write_text(
        json.dumps(
            history,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 60)
    print("TRAINING COMPLETE")
    print(f"Best model: {checkpoint_path}")
    print(f"History: {history_path}")
    print("=" * 60)

    return history
