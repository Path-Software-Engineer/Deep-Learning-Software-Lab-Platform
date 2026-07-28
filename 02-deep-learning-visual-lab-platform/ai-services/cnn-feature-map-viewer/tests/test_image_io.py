from __future__ import annotations

import io

import pytest
from cnn_feature_map_viewer.image_io import ImageValidationError, decode_image
from PIL import Image


def _png(width: int = 36, height: int = 40) -> bytes:
    image = Image.new("L", (width, height), color=128)
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def test_valid_png_is_resized_and_normalized() -> None:
    tensor, metadata = decode_image(_png(), "image/png")

    assert tensor.shape == (1, 1, 28, 28)
    assert metadata["original_shape"] == [40, 36]
    assert metadata["image_data_uri"].startswith("data:image/png;base64,")


@pytest.mark.parametrize(
    ("payload", "media_type", "code"),
    [
        (_png(), "application/octet-stream", "unsupported_media_type"),
        (b"", "image/png", "empty_image"),
        (b"not an image", "image/png", "invalid_image"),
    ],
)
def test_invalid_uploads_fail_with_stable_codes(
    payload: bytes,
    media_type: str,
    code: str,
) -> None:
    with pytest.raises(ImageValidationError) as error:
        decode_image(payload, media_type)

    assert error.value.code == code
