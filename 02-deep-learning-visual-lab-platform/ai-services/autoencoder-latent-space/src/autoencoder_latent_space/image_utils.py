"""Bounded image serialization used by the autoencoder read service."""

from __future__ import annotations

import base64
import io

import torch
from PIL import Image


def pixels_to_data_uri(pixels: torch.Tensor) -> str:
    matrix = pixels.detach().cpu()
    if matrix.ndim == 3:
        matrix = matrix.squeeze(0)
    if tuple(matrix.shape) != (28, 28):
        raise ValueError("Only 28x28 grayscale tensors can be serialized.")
    values = (
        torch.clamp(matrix, 0.0, 1.0)
        .mul(255)
        .round()
        .to(torch.uint8)
        .numpy()
    )
    image = Image.fromarray(values, mode="L")
    stream = io.BytesIO()
    image.save(stream, format="PNG", optimize=True)
    encoded = base64.b64encode(stream.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
