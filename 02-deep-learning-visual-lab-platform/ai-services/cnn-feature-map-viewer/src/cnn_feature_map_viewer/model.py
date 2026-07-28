"""Small registered Fashion-MNIST CNN used for read-only inference."""

from __future__ import annotations

from typing import cast

import torch
from torch import nn

from cnn_feature_map_viewer.config import ModelConfiguration


class FashionCnn(nn.Module):
    """Two-block CNN with stable, allowlisted activation boundaries."""

    def __init__(self, configuration: ModelConfiguration) -> None:
        super().__init__()
        self.configuration = configuration
        self.block1 = nn.Sequential(
            nn.Conv2d(
                configuration.input_channels,
                configuration.conv1_channels,
                kernel_size=3,
                padding=1,
            ),
            nn.BatchNorm2d(configuration.conv1_channels),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.block2 = nn.Sequential(
            nn.Conv2d(
                configuration.conv1_channels,
                configuration.conv2_channels,
                kernel_size=3,
                padding=1,
            ),
            nn.BatchNorm2d(configuration.conv2_channels),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        flattened = configuration.conv2_channels * 7 * 7
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(flattened, configuration.hidden_features),
            nn.ReLU(),
            nn.Dropout(configuration.dropout),
            nn.Linear(configuration.hidden_features, configuration.class_count),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        features = self.block1(inputs)
        features = self.block2(features)
        return cast(torch.Tensor, self.classifier(features))

    @property
    def observable_layers(self) -> dict[str, nn.Module]:
        return {
            "block1_relu": self.block1[2],
            "block2_relu": self.block2[2],
        }

    @property
    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())
