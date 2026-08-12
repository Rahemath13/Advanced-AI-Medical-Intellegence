from torch import nn
from torchvision.models import (
    EfficientNet_B0_Weights,
    efficientnet_b0,
)

NUM_CLASSES = 2


def create_model(
    pretrained: bool = True,
) -> nn.Module:
    """
    Create an EfficientNet-B0 classifier.

    Classes:
        0 -> NORMAL
        1 -> PNEUMONIA
    """

    weights = EfficientNet_B0_Weights.DEFAULT if pretrained else None

    model = efficientnet_b0(
        weights=weights,
    )

    input_features = model.classifier[1].in_features

    model.classifier[1] = nn.Linear(
        input_features,
        NUM_CLASSES,
    )

    return model
