import csv
import random
import re
from pathlib import Path

SOURCE_DIR = Path("data/raw/train")
OUTPUT_FILE = Path("data/train_val_manifest.csv")

CLASS_NAMES = [
    "NORMAL",
    "PNEUMONIA",
]

VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}

VALIDATION_RATIO = 0.10
RANDOM_SEED = 42


def get_group_id(image_path: Path) -> str:
    """
    Extract a patient/study group identifier when available.

    Pneumonia images commonly contain identifiers such as
    person1234 in their filenames. Normal images without such
    identifiers are treated as individual groups.
    """

    match = re.search(
        r"(person\d+)",
        image_path.stem.lower(),
    )

    if match:
        return match.group(1)

    return image_path.stem


def collect_images() -> list[dict[str, str]]:
    """Collect image paths, labels, and grouping identifiers."""

    records: list[dict[str, str]] = []

    for label, class_name in enumerate(CLASS_NAMES):
        class_directory = SOURCE_DIR / class_name

        if not class_directory.exists():
            raise FileNotFoundError(f"Missing directory: {class_directory}")

        for image_path in class_directory.rglob("*"):
            if image_path.is_file() and image_path.suffix.lower() in VALID_EXTENSIONS:
                records.append(
                    {
                        "path": str(image_path),
                        "class_name": class_name,
                        "label": str(label),
                        "group": get_group_id(image_path),
                    }
                )

    if not records:
        raise ValueError(f"No images found in {SOURCE_DIR}")

    return records


def split_by_class(
    records: list[dict[str, str]],
    validation_ratio: float,
    random_seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Create a deterministic group-aware train/validation split.

    Groups are never divided between train and validation.
    """

    rng = random.Random(random_seed)

    train_records: list[dict[str, str]] = []
    validation_records: list[dict[str, str]] = []

    for class_name in CLASS_NAMES:
        class_records = [
            record for record in records if record["class_name"] == class_name
        ]

        groups: dict[str, list[dict[str, str]]] = {}

        for record in class_records:
            groups.setdefault(record["group"], []).append(record)

        group_items = list(groups.items())
        rng.shuffle(group_items)

        target_validation_count = max(
            1,
            round(len(class_records) * validation_ratio),
        )

        current_validation_count = 0

        for group_id, group_records in group_items:
            if current_validation_count < target_validation_count:
                validation_records.extend(group_records)
                current_validation_count += len(group_records)
            else:
                train_records.extend(group_records)

    rng.shuffle(train_records)
    rng.shuffle(validation_records)

    return train_records, validation_records


def write_manifest(
    train_records: list[dict[str, str]],
    validation_records: list[dict[str, str]],
) -> None:
    """Write train/validation records to a CSV manifest."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "path",
                "class_name",
                "label",
                "group",
                "split",
            ],
        )

        writer.writeheader()

        for record in train_records:
            writer.writerow(
                {
                    **record,
                    "split": "train",
                }
            )

        for record in validation_records:
            writer.writerow(
                {
                    **record,
                    "split": "validation",
                }
            )


def main() -> None:
    """Create the reproducible training/validation manifest."""

    records = collect_images()

    train_records, validation_records = split_by_class(
        records,
        validation_ratio=VALIDATION_RATIO,
        random_seed=RANDOM_SEED,
    )

    write_manifest(
        train_records,
        validation_records,
    )

    print("=" * 60)
    print("TRAIN / VALIDATION SPLIT")
    print("=" * 60)
    print(f"Original training images : {len(records)}")
    print(f"Training images          : {len(train_records)}")
    print(f"Validation images       : {len(validation_records)}")
    print(f"Manifest                : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
