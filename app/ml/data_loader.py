from pathlib import Path

from torch.utils.data import DataLoader

from app.ml.dataset import MedicalImageDataset
from app.ml.preprocessing import (
    get_train_transforms,
    get_validation_transforms,
)

CLASS_NAMES = [
    "NORMAL",
    "PNEUMONIA",
]

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def collect_samples(
    directory: Path,
    class_names: list[str],
) -> list[tuple[Path, int]]:
    """Collect image paths and integer class labels."""

    samples: list[tuple[Path, int]] = []

    for label, class_name in enumerate(class_names):
        class_directory = directory / class_name

        if not class_directory.exists():
            raise FileNotFoundError(f"Missing class directory: {class_directory}")

        for image_path in class_directory.rglob("*"):
            if image_path.is_file() and image_path.suffix.lower() in IMAGE_EXTENSIONS:
                samples.append((image_path, label))

    if not samples:
        raise ValueError(f"No images found in {directory}")

    return samples


def create_dataloaders(
    data_directory: str = "data/raw",
    batch_size: int = 32,
    num_workers: int = 0,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    """Create train, validation, and test DataLoaders."""

    root = Path(data_directory)

    train_samples = collect_samples(
        root / "train",
        CLASS_NAMES,
    )

    validation_samples = collect_samples(
        root / "val",
        CLASS_NAMES,
    )

    test_samples = collect_samples(
        root / "test",
        CLASS_NAMES,
    )

    train_dataset = MedicalImageDataset(
        train_samples,
        transform=get_train_transforms(),
    )

    validation_dataset = MedicalImageDataset(
        validation_samples,
        transform=get_validation_transforms(),
    )

    test_dataset = MedicalImageDataset(
        test_samples,
        transform=get_validation_transforms(),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=False,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )

    return (
        train_loader,
        validation_loader,
        test_loader,
    )
