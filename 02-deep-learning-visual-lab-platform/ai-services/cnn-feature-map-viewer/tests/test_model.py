from __future__ import annotations

import torch
from cnn_feature_map_viewer.config import MODEL_CONFIGURATION
from cnn_feature_map_viewer.hooks import run_with_activations
from cnn_feature_map_viewer.model import FashionCnn


def test_model_exposes_expected_feature_map_shapes() -> None:
    torch.manual_seed(20260728)
    model = FashionCnn(MODEL_CONFIGURATION)

    logits, activations = run_with_activations(
        model,
        torch.zeros((2, 1, 28, 28), dtype=torch.float32),
        ("block1_relu", "block2_relu"),
    )

    assert logits.shape == (2, 10)
    assert activations["block1_relu"].shape == (2, 16, 28, 28)
    assert activations["block2_relu"].shape == (2, 32, 14, 14)
    assert model.parameter_count == 207_018


def test_activation_hooks_are_removed_after_each_forward() -> None:
    model = FashionCnn(MODEL_CONFIGURATION)
    inputs = torch.zeros((1, 1, 28, 28), dtype=torch.float32)

    for _ in range(3):
        run_with_activations(model, inputs, ("block1_relu",))

    assert len(model.observable_layers["block1_relu"]._forward_hooks) == 0
    assert len(model.observable_layers["block2_relu"]._forward_hooks) == 0


def test_unknown_activation_layer_is_rejected() -> None:
    model = FashionCnn(MODEL_CONFIGURATION)

    try:
        run_with_activations(
            model,
            torch.zeros((1, 1, 28, 28)),
            ("unknown",),
        )
    except ValueError as error:
        assert "Unknown observable layer" in str(error)
    else:
        raise AssertionError("Unknown layer should fail before inference.")
