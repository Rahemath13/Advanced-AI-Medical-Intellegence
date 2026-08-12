import torch

from app.ml.evaluator import evaluate_model


class DummyModel(torch.nn.Module):
    """Simple model for evaluator testing."""

    def forward(self, images):
        batch_size = images.shape[0]

        return torch.tensor(
            [
                [4.0, 1.0],
                [1.0, 4.0],
                [4.0, 1.0],
                [1.0, 4.0],
            ][:batch_size]
        )


def test_evaluate_model():
    images = torch.randn(
        4,
        3,
        224,
        224,
    )

    targets = torch.tensor([0, 1, 0, 1])

    dataset = torch.utils.data.TensorDataset(
        images,
        targets,
    )

    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=4,
    )

    model = DummyModel()

    metrics = evaluate_model(
        model=model,
        data_loader=loader,
        device=torch.device("cpu"),
    )

    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["specificity"] == 1.0
    assert metrics["f1_score"] == 1.0
