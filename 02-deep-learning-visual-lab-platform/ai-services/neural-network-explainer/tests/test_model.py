from __future__ import annotations

import torch
from neural_network_explainer.dataset import xor_tensors
from neural_network_explainer.model import ExplainableXorMlp


def test_model_exposes_the_expected_architecture_and_state() -> None:
    model = ExplainableXorMlp()
    features, _ = xor_tensors()
    output, state = model.forward_with_state(features)
    assert model.parameter_count == 17
    assert output.shape == (4, 1)
    assert state["hidden_activations"].shape == (4, 4)
    assert torch.equal(model(features), output)
