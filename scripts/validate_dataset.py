from pathlib import Path

from PIL import Image
from PIL.Image import UnidentifiedImageError

DATA_DIR = Path("data/raw")

SPLITS = [
    "train",
    "val",
    "test",
]

CLASS_NAMES = [
    "NORMAL",
    "PNEUMONIA",
]

VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def validate_image(image_path: Path) -> bool:
    """Validate that an image can be opened and verified."""

    try:
        with Image.open(image_path) as image:
            image.verify()

        return True

    except (UnidentifiedImageError, OSError):
        return False


def validate_dataset() -> None:
    """Validate dataset structure, images, and class distribution."""

    total_valid = 0
    total_invalid = 0

    print("=" * 60)
    print("MEDICAL DATASET VALIDATION")
    print("=" * 60)

    for split in SPLITS:
        print(f"\n[{split.upper()}]")

        split_total = 0

        for class_name in CLASS_NAMES:
            class_directory = DATA_DIR / split / class_name

            if not class_directory.exists():
                raise FileNotFoundError(f"Missing directory: {class_directory}")

            images = [
                path
                for path in class_directory.rglob("*")
                if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
            ]

            valid_count = 0
            invalid_count = 0

            for image_path in images:
                if validate_image(image_path):
                    valid_count += 1
                else:
                    invalid_count += 1
                    print(f"Invalid image: {image_path}")

            split_total += valid_count
            total_valid += valid_count
            total_invalid += invalid_count

            print(f"{class_name:<10} Valid: {valid_count:<5} Invalid: {invalid_count}")

        print(f"Split total: {split_total}")

    print("\n" + "=" * 60)
    print(f"TOTAL VALID IMAGES: {total_valid}")
    print(f"TOTAL INVALID IMAGES: {total_invalid}")
    print("=" * 60)

    if total_invalid > 0:
        raise ValueError(f"Dataset contains {total_invalid} invalid images.")


if __name__ == "__main__":
    validate_dataset()
