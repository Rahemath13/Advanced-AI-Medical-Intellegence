import torch

from app.ml.trainer import (
    calculate_accuracy,
    get_device,
)


def test_calculate_accuracy():
    outputs = torch.tensor(
        [
            [3.0, 1.0],
            [1.0, 4.0],
            [5.0, 2.0],
        ]
    )

    targets = torch.tensor([0, 1, 1])

    accuracy = calculate_accuracy(
        outputs,
        targets,
    )

    assert accuracy == 2 / 3


def test_get_device_auto():
    device = get_device("auto")

    assert device.type in {
        "cpu",
        "cuda",
    }
