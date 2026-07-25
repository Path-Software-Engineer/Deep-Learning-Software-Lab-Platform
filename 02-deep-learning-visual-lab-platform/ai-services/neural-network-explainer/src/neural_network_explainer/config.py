"""Stable configuration values for the registered Sprint 1 model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

MODEL_VERSION = "xor-mlp-v1"
LIMITATIONS = (
    "The XOR dataset is a controlled educational example, not a production benchmark.",
    "Perfect accuracy on four observations is not evidence of generalization.",
    "Internal activations are inspectable values, not causal explanations.",
)


@dataclass(frozen=True, slots=True)
class ModelConfiguration:
    input_size: int = 2
    hidden_size: int = 4
    output_size: int = 1
    hidden_activation: str = "tanh"
    output_activation: str = "sigmoid"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TrainingConfiguration:
    seed: int = 190
    epochs: int = 2000
    learning_rate: float = 0.05
    optimizer: str = "Adam"
    loss_function: str = "BCELoss"
    history_interval: int = 10
    threshold: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
