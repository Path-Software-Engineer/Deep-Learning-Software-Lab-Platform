"""Convolutional autoencoder with an intentionally visible 2D bottleneck."""

from __future__ import annotations

from typing import cast

import torch
from torch import nn

from autoencoder_latent_space.config import ModelConfiguration


class FashionAutoencoder(nn.Module):
    """Encode 28x28 grayscale images to two coordinates and decode them."""

    def __init__(self, configuration: ModelConfiguration) -> None:
        super().__init__()
        self.configuration = configuration
        self.encoder_convolution = nn.Sequential(
            nn.Conv2d(
                configuration.input_channels,
                configuration.encoder_channels_one,
                kernel_size=3,
                stride=2,
                padding=1,
            ),
            nn.ReLU(),
            nn.Conv2d(
                configuration.encoder_channels_one,
                configuration.encoder_channels_two,
                kernel_size=3,
                stride=2,
                padding=1,
            ),
            nn.ReLU(),
        )
        flattened = configuration.encoder_channels_two * 7 * 7
        self.encoder_projection = nn.Sequential(
            nn.Flatten(),
            nn.Linear(flattened, configuration.hidden_features),
            nn.ReLU(),
            nn.Linear(configuration.hidden_features, configuration.latent_dimensions),
        )
        self.decoder_projection = nn.Sequential(
            nn.Linear(configuration.latent_dimensions, configuration.hidden_features),
            nn.ReLU(),
            nn.Linear(configuration.hidden_features, flattened),
            nn.ReLU(),
        )
        self.decoder_convolution = nn.Sequential(
            nn.Unflatten(1, (configuration.encoder_channels_two, 7, 7)),
            nn.ConvTranspose2d(
                configuration.encoder_channels_two,
                configuration.encoder_channels_one,
                kernel_size=4,
                stride=2,
                padding=1,
            ),
            nn.ReLU(),
            nn.ConvTranspose2d(
                configuration.encoder_channels_one,
                configuration.input_channels,
                kernel_size=4,
                stride=2,
                padding=1,
            ),
            nn.Sigmoid(),
        )

    def encode(self, inputs: torch.Tensor) -> torch.Tensor:
        features = self.encoder_convolution(inputs)
        return cast(torch.Tensor, self.encoder_projection(features))

    def decode(self, coordinates: torch.Tensor) -> torch.Tensor:
        features = self.decoder_projection(coordinates)
        return cast(torch.Tensor, self.decoder_convolution(features))

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        coordinates = self.encode(inputs)
        return self.decode(coordinates), coordinates

    @property
    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())
