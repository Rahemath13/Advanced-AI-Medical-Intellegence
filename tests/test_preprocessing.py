from PIL import Image

from app.ml.preprocessing import (
    IMAGE_SIZE,
    get_train_transforms,
    get_validation_transforms,
)


def test_train_transform_output_shape():
    image = Image.new(
        "RGB",
        (500, 500),
    )

    transform = get_train_transforms()
    result = transform(image)

    assert result.shape == (
        3,
        IMAGE_SIZE,
        IMAGE_SIZE,
    )


def test_validation_transform_output_shape():
    image = Image.new(
        "RGB",
        (500, 500),
    )

    transform = get_validation_transforms()
    result = transform(image)

    assert result.shape == (
        3,
        IMAGE_SIZE,
        IMAGE_SIZE,
    )
