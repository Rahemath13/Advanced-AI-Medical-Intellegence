import random

from torch.utils.data import DataLoader, Subset

from app.ml.data_loader import create_dataloaders
from app.ml.trainer import train_model
from app.ml.training_config import TrainingConfig


def create_stratified_indices(
    dataset,
    sample_count: int,
    random_seed: int,
) -> list[int]:
    """Create balanced indices across all classes."""

    class_indices: dict[int, list[int]] = {}

    for index, (_, label) in enumerate(dataset.samples):
        class_indices.setdefault(
            int(label),
            [],
        ).append(index)

    if len(class_indices) < 2:
        raise ValueError("Dataset must contain at least two classes.")

    rng = random.Random(random_seed)

    for indices in class_indices.values():
        rng.shuffle(indices)

    classes = list(class_indices)

    samples_per_class = sample_count // len(classes)

    selected: list[int] = []

    for class_id in classes:
        selected.extend(class_indices[class_id][:samples_per_class])

    remaining = sample_count - len(selected)

    if remaining > 0:
        candidates = []

        for class_id in classes:
            candidates.extend(class_indices[class_id][samples_per_class:])

        rng.shuffle(candidates)

        selected.extend(candidates[:remaining])

    rng.shuffle(selected)

    return selected


def create_development_loaders(
    dataset,
    train_count: int,
    validation_count: int,
    batch_size: int,
    random_seed: int,
):
    """
    Create independent stratified development train
    and validation subsets from the original training data.
    """

    total_required = train_count + validation_count

    all_indices = create_stratified_indices(
        dataset,
        total_required,
        random_seed,
    )

    rng = random.Random(random_seed)
    rng.shuffle(all_indices)

    train_indices = all_indices[:train_count]

    validation_indices = all_indices[train_count:]

    train_subset = Subset(
        dataset,
        train_indices,
    )

    validation_subset = Subset(
        dataset,
        validation_indices,
    )

    train_loader = DataLoader(
        train_subset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=False,
    )

    validation_loader = DataLoader(
        validation_subset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )

    return train_loader, validation_loader


def main() -> None:
    """Run the CPU development training pipeline."""

    config = TrainingConfig()

    train_loader, _, _ = create_dataloaders(
        data_directory=config.data_directory,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
    )

    train_loader, validation_loader = create_development_loaders(
        dataset=train_loader.dataset,
        train_count=config.max_train_samples,
        validation_count=config.max_validation_samples,
        batch_size=config.batch_size,
        random_seed=config.random_seed,
    )

    print(f"Development training samples: {len(train_loader.dataset)}")

    print(f"Development validation samples: {len(validation_loader.dataset)}")

    train_model(
        train_loader=train_loader,
        validation_loader=validation_loader,
        config=config,
    )


if __name__ == "__main__":
    main()
