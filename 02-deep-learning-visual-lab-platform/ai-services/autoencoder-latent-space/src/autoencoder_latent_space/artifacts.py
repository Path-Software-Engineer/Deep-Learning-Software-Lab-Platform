"""Integrity-checked loader for registered autoencoder evidence."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import torch

from autoencoder_latent_space.config import (
    CLASS_NAMES,
    DATASET_VERSION,
    MODEL_VERSION,
    REFERENCE_POINTS_PER_CLASS,
    ModelConfiguration,
)
from autoencoder_latent_space.model import FashionAutoencoder


class AutoencoderArtifactIntegrityError(RuntimeError):
    """Raised when registered autoencoder evidence fails closed."""


@dataclass(frozen=True, slots=True)
class AutoencoderArtifactBundle:
    model: FashionAutoencoder
    manifest: dict[str, Any]
    history: dict[str, Any]
    points: tuple[dict[str, Any], ...]
    checkpoint_sha256: str
    checkpoint_bytes: int


def _read_json(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AutoencoderArtifactIntegrityError(
            f"Cannot read registered autoencoder artifact: {path.name}"
        ) from exc
    if not isinstance(document, dict):
        raise AutoencoderArtifactIntegrityError(
            f"Registered autoencoder artifact must be an object: {path.name}"
        )
    return cast(dict[str, Any], document)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(64 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise AutoencoderArtifactIntegrityError(
            f"Cannot read registered autoencoder artifact: {path.name}"
        ) from exc
    return digest.hexdigest()


def _validated_points(
    document: dict[str, Any],
    path: Path,
    expected_sha256: str,
) -> tuple[dict[str, Any], ...]:
    if _sha256(path) != expected_sha256:
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder latent gallery checksum does not match."
        )
    raw_points = document.get("points")
    expected = len(CLASS_NAMES) * REFERENCE_POINTS_PER_CLASS
    if not isinstance(raw_points, list) or len(raw_points) != expected:
        raise AutoencoderArtifactIntegrityError(
            f"Autoencoder latent gallery must contain {expected} points."
        )
    identifiers: set[str] = set()
    validated: list[dict[str, Any]] = []
    for raw in raw_points:
        if not isinstance(raw, dict):
            raise AutoencoderArtifactIntegrityError("Latent point is not an object.")
        point = cast(dict[str, Any], raw)
        identifier = point.get("id")
        label_index = point.get("label_index")
        coordinate = point.get("coordinate")
        pixels = point.get("pixels")
        if not isinstance(identifier, str) or identifier in identifiers:
            raise AutoencoderArtifactIntegrityError(
                "Latent point IDs must be unique strings."
            )
        if not isinstance(label_index, int) or label_index not in range(len(CLASS_NAMES)):
            raise AutoencoderArtifactIntegrityError("Latent point label is invalid.")
        if (
            not isinstance(coordinate, list)
            or len(coordinate) != 2
            or any(
                not isinstance(value, (int, float)) or not math.isfinite(value)
                for value in coordinate
            )
        ):
            raise AutoencoderArtifactIntegrityError(
                "Latent point coordinate must contain two finite values."
            )
        if (
            not isinstance(pixels, list)
            or len(pixels) != 28
            or any(not isinstance(row, list) or len(row) != 28 for row in pixels)
        ):
            raise AutoencoderArtifactIntegrityError(
                "Latent point pixels must be a 28x28 matrix."
            )
        identifiers.add(identifier)
        validated.append(point)
    return tuple(validated)


def load_autoencoder_artifact_bundle(
    directory: Path,
) -> AutoencoderArtifactBundle:
    manifest = _read_json(directory / "manifest.json")
    history = _read_json(directory / "training-history.json")
    gallery_path = directory / "latent-gallery.json"
    gallery = _read_json(gallery_path)
    if manifest.get("model_version") != MODEL_VERSION:
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder manifest model version is not registered."
        )
    if manifest.get("dataset_version") != DATASET_VERSION:
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder manifest dataset version is not registered."
        )
    if history.get("model_version") != MODEL_VERSION:
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder history does not match the model."
        )
    if gallery.get("model_version") != MODEL_VERSION:
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder latent gallery does not match the model."
        )
    checkpoint = directory / str(manifest.get("checkpoint", ""))
    if not checkpoint.is_file():
        raise AutoencoderArtifactIntegrityError(
            "Registered autoencoder checkpoint is missing."
        )
    checkpoint_sha256 = _sha256(checkpoint)
    if checkpoint_sha256 != manifest.get("checkpoint_sha256"):
        raise AutoencoderArtifactIntegrityError(
            "Registered autoencoder checkpoint checksum does not match."
        )
    checkpoint_bytes = checkpoint.stat().st_size
    if checkpoint_bytes != manifest.get("checkpoint_bytes"):
        raise AutoencoderArtifactIntegrityError(
            "Registered autoencoder checkpoint size does not match."
        )
    model_data = manifest.get("model_configuration")
    training_data = manifest.get("training_configuration")
    if not isinstance(model_data, dict) or not isinstance(training_data, dict):
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder manifest configuration is invalid."
        )
    if history.get("configuration") != training_data:
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder history configuration does not match."
        )
    model = FashionAutoencoder(ModelConfiguration(**model_data))
    try:
        payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
        if payload["model_configuration"] != model_data:
            raise AutoencoderArtifactIntegrityError(
                "Autoencoder checkpoint model contract does not match."
            )
        if payload["training_configuration"] != training_data:
            raise AutoencoderArtifactIntegrityError(
                "Autoencoder checkpoint training contract does not match."
            )
        if payload["dataset_version"] != DATASET_VERSION:
            raise AutoencoderArtifactIntegrityError(
                "Autoencoder checkpoint dataset contract does not match."
            )
        model.load_state_dict(payload["model_state_dict"], strict=True)
    except (OSError, KeyError, RuntimeError, TypeError) as exc:
        raise AutoencoderArtifactIntegrityError(
            "Registered autoencoder checkpoint cannot be loaded."
        ) from exc
    model.eval()
    gallery_sha256 = manifest.get("latent_gallery_sha256")
    if not isinstance(gallery_sha256, str):
        raise AutoencoderArtifactIntegrityError(
            "Autoencoder latent gallery checksum is missing."
        )
    return AutoencoderArtifactBundle(
        model=model,
        manifest=manifest,
        history=history,
        points=_validated_points(gallery, gallery_path, gallery_sha256),
        checkpoint_sha256=checkpoint_sha256,
        checkpoint_bytes=checkpoint_bytes,
    )
