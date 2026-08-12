from pathlib import Path

from PIL import Image
from torch.utils.data import Dataset


class MedicalImageDataset(Dataset):
    """PyTorch dataset for labeled medical images."""

    def __init__(
        self,
        samples: list[tuple[Path, int]],
        transform=None,
    ) -> None:
        self.samples = samples
        self.transform = transform

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        image_path, label = self.samples[index]

        image = Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label
