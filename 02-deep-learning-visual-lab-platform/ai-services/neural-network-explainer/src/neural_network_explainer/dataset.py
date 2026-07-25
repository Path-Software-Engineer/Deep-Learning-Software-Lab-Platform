"""Controlled XOR data contract used by the Sprint 1 explainer."""

from __future__ import annotations

import torch

XOR_POINTS: tuple[tuple[float, float], ...] = (
    (0.0, 0.0),
    (0.0, 1.0),
    (1.0, 0.0),
    (1.0, 1.0),
)
XOR_LABELS: tuple[int, ...] = (0, 1, 1, 0)


def validate_xor_inputs(inputs: tuple[float, float]) -> tuple[float, float]:
    if len(inputs) != 2:
        raise ValueError("XOR requires exactly two inputs.")
    if any(value not in (0.0, 1.0) for value in inputs):
        raise ValueError("Each XOR input must be 0 or 1.")
    return inputs


def xor_target(inputs: tuple[float, float]) -> int:
    first, second = validate_xor_inputs(inputs)
    return int(bool(first) ^ bool(second))


def xor_tensors() -> tuple[torch.Tensor, torch.Tensor]:
    return (
        torch.tensor(XOR_POINTS, dtype=torch.float32),
        torch.tensor(XOR_LABELS, dtype=torch.float32).unsqueeze(1),
    )
