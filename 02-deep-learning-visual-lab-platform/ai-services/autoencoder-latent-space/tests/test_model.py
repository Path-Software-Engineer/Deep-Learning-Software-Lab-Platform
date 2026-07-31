from __future__ import annotations

import torch
from autoencoder_latent_space.config import MODEL_CONFIGURATION
from autoencoder_latent_space.model import FashionAutoencoder


def test_autoencoder_exposes_expected_shapes_and_range() -> None:
    torch.manual_seed(20_260_729)
    model = FashionAutoencoder(MODEL_CONFIGURATION)
    inputs = torch.zeros((3, 1, 28, 28), dtype=torch.float32)

    reconstructed, coordinates = model(inputs)

    assert reconstructed.shape == inputs.shape
    assert coordinates.shape == (3, 2)
    assert float(reconstructed.detach().min()) >= 0.0
    assert float(reconstructed.detach().max()) <= 1.0
    assert model.parameter_count == 215_923


def test_encode_decode_boundaries_are_composable() -> None:
    model = FashionAutoencoder(MODEL_CONFIGURATION)
    inputs = torch.rand((2, 1, 28, 28), dtype=torch.float32)

    coordinates = model.encode(inputs)
    reconstructed = model.decode(coordinates)

    assert coordinates.shape == (2, 2)
    assert reconstructed.shape == inputs.shape
