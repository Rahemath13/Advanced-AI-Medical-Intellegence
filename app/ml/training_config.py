from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingConfig:
    """Configuration for model training."""

    data_directory: str = "data/raw"
    manifest_path: str = "data/train_val_manifest.csv"

    image_size: int = 224
    batch_size: int = 16

    epochs: int = 5
    learning_rate: float = 1e-4
    weight_decay: float = 1e-4

    patience: int = 2

    random_seed: int = 42

    num_workers: int = 0

    checkpoint_directory: str = "models/checkpoints"
    best_model_name: str = "best_efficientnet_b0.pth"

    device: str = "auto"

    # CPU development mode
    max_train_samples: int | None = 800
    max_validation_samples: int | None = 200
