"""Small PyTorch MLP with an explicit, inspectable forward state."""

from __future__ import annotations

from typing import TypedDict

import torch
from torch import nn

from neural_network_explainer.config import ModelConfiguration


class ForwardState(TypedDict):
    hidden_preactivations: torch.Tensor
    hidden_activations: torch.Tensor
    output_preactivations: torch.Tensor
    output_activations: torch.Tensor


class ExplainableXorMlp(nn.Module):
    def __init__(self, configuration: ModelConfiguration | None = None) -> None:
        super().__init__()
        self.configuration = configuration or ModelConfiguration()
        self.hidden = nn.Linear(
            self.configuration.input_size,
            self.configuration.hidden_size,
        )
        self.output = nn.Linear(
            self.configuration.hidden_size,
            self.configuration.output_size,
        )

    @property
    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())

    def forward_with_state(
        self,
        features: torch.Tensor,
    ) -> tuple[torch.Tensor, ForwardState]:
        hidden_preactivations = self.hidden(features)
        hidden_activations = torch.tanh(hidden_preactivations)
        output_preactivations = self.output(hidden_activations)
        output_activations = torch.sigmoid(output_preactivations)
        state: ForwardState = {
            "hidden_preactivations": hidden_preactivations,
            "hidden_activations": hidden_activations,
            "output_preactivations": output_preactivations,
            "output_activations": output_activations,
        }
        return output_activations, state

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        output, _ = self.forward_with_state(features)
        return output
