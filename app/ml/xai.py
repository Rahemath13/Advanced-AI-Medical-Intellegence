from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import (
    show_cam_on_image,
)
from torchvision import transforms

from app.ml.model import create_model

CLASS_NAMES = [
    "NORMAL",
    "PNEUMONIA",
]


def load_xai_model(
    checkpoint_path: str | Path,
    device: torch.device,
):
    """Load the trained model for Grad-CAM."""

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


def get_target_layer(model):
    """Return the final convolutional layer."""

    return model.features[-1]


def preprocess_image(
    image_path: str | Path,
):
    """Prepare a chest X-ray for model inference."""

    image = Image.open(image_path).convert("RGB")

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[
                    0.485,
                    0.456,
                    0.406,
                ],
                std=[
                    0.229,
                    0.224,
                    0.225,
                ],
            ),
        ]
    )

    tensor = transform(image).unsqueeze(0)

    return image, tensor


def generate_gradcam(
    model,
    image_tensor: torch.Tensor,
    device: torch.device,
    target_class: int | None = None,
):
    """Generate a Grad-CAM heatmap."""

    image_tensor = image_tensor.to(device)

    target_layer = get_target_layer(model)

    with torch.no_grad():
        output = model(image_tensor)

        probabilities = torch.softmax(
            output,
            dim=1,
        )

        predicted_class = int(probabilities.argmax(dim=1).item())

    if target_class is None:
        target_class = predicted_class

    cam = GradCAM(
        model=model,
        target_layers=[target_layer],
    )

    grayscale_cam = cam(
        input_tensor=image_tensor,
    )[0]

    return (
        grayscale_cam,
        predicted_class,
        probabilities[0].cpu().numpy(),
    )


def create_overlay(
    image: Image.Image,
    grayscale_cam: np.ndarray,
):
    """Overlay Grad-CAM heatmap on the original image."""

    rgb_image = np.asarray(image.resize((224, 224))).astype(np.float32) / 255.0

    visualization = show_cam_on_image(
        rgb_image,
        grayscale_cam,
        use_rgb=True,
    )

    return visualization


def save_gradcam(
    visualization: np.ndarray,
    output_path: str | Path,
):
    """Save Grad-CAM visualization."""

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    visualization_bgr = cv2.cvtColor(
        visualization,
        cv2.COLOR_RGB2BGR,
    )

    cv2.imwrite(
        str(output_path),
        visualization_bgr,
    )
