"""Bounded image decoding and serialization for CNN inference."""

from __future__ import annotations

import base64
import io
from dataclasses import asdict
from typing import Any

import torch
from PIL import Image, UnidentifiedImageError

from cnn_feature_map_viewer.config import (
    ALLOWED_MEDIA_TYPES,
    MAX_IMAGE_BYTES,
    MAX_IMAGE_DIMENSION,
    PREPROCESSING_CONFIGURATION,
)
from cnn_feature_map_viewer.dataset import normalize


class ImageValidationError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def pixels_to_data_uri(pixels: torch.Tensor) -> str:
    bounded = torch.clamp(pixels.squeeze(0), 0.0, 1.0)
    payload = (bounded * 255).round().to(torch.uint8).flatten().tolist()
    image = Image.new("L", (28, 28))
    image.putdata(payload)
    stream = io.BytesIO()
    image.save(stream, format="PNG", optimize=True)
    encoded = base64.b64encode(stream.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def decode_image(payload: bytes, media_type: str | None) -> tuple[torch.Tensor, dict[str, Any]]:
    normalized_media_type = (media_type or "").split(";", 1)[0].strip().lower()
    if normalized_media_type not in ALLOWED_MEDIA_TYPES:
        raise ImageValidationError(
            "unsupported_media_type",
            "Upload a PNG or JPEG image.",
        )
    if not payload:
        raise ImageValidationError("empty_image", "The uploaded image is empty.")
    if len(payload) > MAX_IMAGE_BYTES:
        raise ImageValidationError(
            "image_too_large",
            f"The image exceeds the {MAX_IMAGE_BYTES} byte limit.",
        )
    try:
        with Image.open(io.BytesIO(payload)) as source:
            source.verify()
        with Image.open(io.BytesIO(payload)) as source:
            width, height = source.size
            if width < 1 or height < 1:
                raise ImageValidationError("invalid_dimensions", "Image dimensions are invalid.")
            if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
                raise ImageValidationError(
                    "image_dimensions_too_large",
                    f"Image dimensions cannot exceed {MAX_IMAGE_DIMENSION}px.",
                )
            grayscale = source.convert("L")
            resized = grayscale.resize((28, 28), Image.Resampling.BILINEAR)
            pixels = torch.tensor(list(resized.getdata()), dtype=torch.float32)
    except ImageValidationError:
        raise
    except (OSError, UnidentifiedImageError) as exc:
        raise ImageValidationError(
            "invalid_image",
            "The uploaded bytes are not a valid PNG or JPEG image.",
        ) from exc

    pixels = (pixels.reshape(1, 28, 28) / 255.0).contiguous()
    return normalize(pixels).unsqueeze(0), {
        "source": "upload",
        "original_shape": [height, width],
        "tensor_shape": [1, 1, 28, 28],
        "preprocessing": asdict(PREPROCESSING_CONFIGURATION),
        "image_data_uri": pixels_to_data_uri(pixels),
    }
