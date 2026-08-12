import torch

from app.ml.model import create_model


def test_model_output_shape():
    model = create_model(pretrained=False)

    model.eval()

    inputs = torch.randn(
        2,
        3,
        224,
        224,
    )

    with torch.no_grad():
        outputs = model(inputs)

    assert outputs.shape == (2, 2)


def test_model_has_two_classes():
    model = create_model(pretrained=False)

    assert model.classifier[1].out_features == 2
