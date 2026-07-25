from __future__ import annotations

from pathlib import Path

import pytest
from neural_network_explainer.service import NeuralNetworkExplainer


@pytest.fixture
def service(artifact_directory: Path) -> NeuralNetworkExplainer:
    return NeuralNetworkExplainer(artifact_directory)


def test_summary_describes_the_registered_pytorch_model(
    service: NeuralNetworkExplainer,
) -> None:
    summary = service.summary()
    assert summary["engine"] == "PyTorch"
    assert summary["model_version"] == "xor-mlp-v1"
    assert summary["architecture"]["parameter_count"] == 17
    assert summary["dataset"]["labels"] == [0, 1, 1, 0]


@pytest.mark.parametrize(
    ("inputs", "expected"),
    [((0.0, 0.0), 0), ((0.0, 1.0), 1), ((1.0, 0.0), 1), ((1.0, 1.0), 0)],
)
def test_registered_model_solves_the_controlled_xor_set(
    service: NeuralNetworkExplainer,
    inputs: tuple[float, float],
    expected: int,
) -> None:
    trace = service.forward(inputs)
    assert trace["prediction"] == expected
    assert trace["target"] == expected
    assert [layer["id"] for layer in trace["layers"]] == ["hidden", "output"]
    assert trace["checkpoint_sha256"] == service.summary()["checkpoint"]["sha256"]


def test_training_history_is_registered_evidence(
    service: NeuralNetworkExplainer,
) -> None:
    history = service.training_history()
    assert history["seed"] == 190
    assert history["configuration"]["optimizer"] == "Adam"
    assert history["configuration"]["epochs"] == 2000
    assert history["metrics"]["accuracy"] == 1.0


def test_invalid_forward_input_is_rejected(service: NeuralNetworkExplainer) -> None:
    with pytest.raises(ValueError, match="must be 0 or 1"):
        service.forward((0.25, 1.0))
