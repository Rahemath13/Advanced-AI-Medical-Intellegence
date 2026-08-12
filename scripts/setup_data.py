import random
import shutil
from pathlib import Path

RANDOM_SEED = 42

SOURCE_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")

CLASS_NAMES = [
    "NORMAL",
    "PNEUMONIA",
]

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def collect_images(directory: Path) -> list[Path]:
    """Collect supported image files recursively."""

    return [
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]


def prepare_dataset() -> None:
    """Create train/validation/test directory structure."""

    random.seed(RANDOM_SEED)

    for class_name in CLASS_NAMES:
        source_class_dir = SOURCE_DIR / class_name

        if not source_class_dir.exists():
            raise FileNotFoundError(f"Missing dataset directory: {source_class_dir}")

        images = collect_images(source_class_dir)

        if not images:
            raise ValueError(f"No images found for class: {class_name}")

        random.shuffle(images)

        total = len(images)

        train_end = int(total * 0.70)
        validation_end = int(total * 0.85)

        splits = {
            "train": images[:train_end],
            "validation": images[train_end:validation_end],
            "test": images[validation_end:],
        }

        for split_name, split_images in splits.items():
            destination = OUTPUT_DIR / split_name / class_name

            destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            for image_path in split_images:
                shutil.copy2(
                    image_path,
                    destination / image_path.name,
                )

            print(f"{class_name} | {split_name}: {len(split_images)} images")


if __name__ == "__main__":
    prepare_dataset()
