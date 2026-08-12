import argparse
from pathlib import Path

import torch

from app.ml.xai import (
    create_overlay,
    generate_gradcam,
    load_xai_model,
    preprocess_image,
    save_gradcam,
)


def main() -> None:
    """Generate a Grad-CAM explanation."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image",
        required=True,
        help="Path to chest X-ray image.",
    )

    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    checkpoint = Path("models/checkpoints/best_efficientnet_b0.pth")

    image_path = Path(args.image)

    model = load_xai_model(
        checkpoint,
        device,
    )

    image, image_tensor = preprocess_image(image_path)

    grayscale_cam, predicted_class, probabilities = generate_gradcam(
        model=model,
        image_tensor=image_tensor,
        device=device,
    )

    visualization = create_overlay(
        image,
        grayscale_cam,
    )

    output_path = Path("models/xai") / f"{image_path.stem}_gradcam.jpg"

    save_gradcam(
        visualization,
        output_path,
    )

    print("=" * 60)
    print("GRAD-CAM EXPLANATION")
    print("=" * 60)

    print(f"Prediction: {'PNEUMONIA' if predicted_class == 1 else 'NORMAL'}")

    print(f"Normal probability: {probabilities[0]:.4f}")

    print(f"Pneumonia probability: {probabilities[1]:.4f}")

    print(f"Explanation saved to: {output_path}")


if __name__ == "__main__":
    main()
