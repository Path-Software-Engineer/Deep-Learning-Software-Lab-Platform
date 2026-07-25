"""Serialize model parameters and forward values without recomputing them."""

from __future__ import annotations

from typing import Any

import torch

from neural_network_explainer.model import ExplainableXorMlp, ForwardState


def _vector(tensor: torch.Tensor) -> list[float]:
    return [float(value) for value in tensor.detach().cpu().reshape(-1).tolist()]


def _matrix(tensor: torch.Tensor) -> list[list[float]]:
    return [[float(value) for value in row] for row in tensor.detach().cpu().tolist()]


def build_layer_snapshot(
    model: ExplainableXorMlp,
    state: ForwardState,
) -> list[dict[str, Any]]:
    return [
        {
            "id": "hidden",
            "label": "Hidden layer",
            "operation": "Linear + tanh",
            "weights": _matrix(model.hidden.weight),
            "biases": _vector(model.hidden.bias),
            "preactivations": _vector(state["hidden_preactivations"]),
            "activations": _vector(state["hidden_activations"]),
        },
        {
            "id": "output",
            "label": "Output layer",
            "operation": "Linear + sigmoid",
            "weights": _matrix(model.output.weight),
            "biases": _vector(model.output.bias),
            "preactivations": _vector(state["output_preactivations"]),
            "activations": _vector(state["output_activations"]),
        },
    ]
