"""Integrity-checked loader for the registered CNN evidence bundle."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import torch

from cnn_feature_map_viewer.config import (
    CLASS_NAMES,
    DATASET_VERSION,
    MODEL_VERSION,
    ModelConfiguration,
)
from cnn_feature_map_viewer.model import FashionCnn


class CnnArtifactIntegrityError(RuntimeError):
    """Raised when registered CNN evidence cannot be trusted."""


@dataclass(frozen=True, slots=True)
class CnnArtifactBundle:
    model: FashionCnn
    manifest: dict[str, Any]
    history: dict[str, Any]
    samples: tuple[dict[str, Any], ...]
    checkpoint_sha256: str
    checkpoint_bytes: int


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CnnArtifactIntegrityError(
            f"Cannot read registered CNN artifact: {path.name}"
        ) from exc
    if not isinstance(value, dict):
        raise CnnArtifactIntegrityError(
            f"Registered CNN artifact must be an object: {path.name}"
        )
    return cast(dict[str, Any], value)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(64 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise CnnArtifactIntegrityError(
            f"Cannot read registered CNN artifact: {path.name}"
        ) from exc
    return digest.hexdigest()


def _validated_samples(
    samples_document: dict[str, Any],
    expected_sha256: str,
    samples_path: Path,
) -> tuple[dict[str, Any], ...]:
    if _sha256(samples_path) != expected_sha256:
        raise CnnArtifactIntegrityError("CNN sample gallery checksum does not match.")
    raw_samples = samples_document.get("samples")
    if not isinstance(raw_samples, list) or len(raw_samples) != len(CLASS_NAMES):
        raise CnnArtifactIntegrityError("CNN sample gallery must contain one sample per class.")
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for raw in raw_samples:
        if not isinstance(raw, dict):
            raise CnnArtifactIntegrityError("CNN sample gallery entry is invalid.")
        sample = cast(dict[str, Any], raw)
        sample_id = sample.get("id")
        label_index = sample.get("label_index")
        pixels = sample.get("pixels")
        if not isinstance(sample_id, str) or sample_id in ids:
            raise CnnArtifactIntegrityError("CNN sample IDs must be unique strings.")
        if not isinstance(label_index, int) or label_index not in range(len(CLASS_NAMES)):
            raise CnnArtifactIntegrityError("CNN sample label is invalid.")
        if (
            not isinstance(pixels, list)
            or len(pixels) != 28
            or any(not isinstance(row, list) or len(row) != 28 for row in pixels)
        ):
            raise CnnArtifactIntegrityError("CNN sample pixels must be a 28x28 matrix.")
        ids.add(sample_id)
        result.append(sample)
    return tuple(result)


def load_cnn_artifact_bundle(directory: Path) -> CnnArtifactBundle:
    manifest = _read_json(directory / "manifest.json")
    history = _read_json(directory / "training-history.json")
    samples_path = directory / "sample-gallery.json"
    samples_document = _read_json(samples_path)

    if manifest.get("model_version") != MODEL_VERSION:
        raise CnnArtifactIntegrityError("CNN manifest model version is not registered.")
    if manifest.get("dataset_version") != DATASET_VERSION:
        raise CnnArtifactIntegrityError("CNN manifest dataset version is not registered.")
    if history.get("model_version") != MODEL_VERSION:
        raise CnnArtifactIntegrityError("CNN history does not match the registered model.")
    if samples_document.get("model_version") != MODEL_VERSION:
        raise CnnArtifactIntegrityError("CNN sample gallery does not match the model.")

    checkpoint = directory / str(manifest.get("checkpoint", ""))
    if not checkpoint.is_file():
        raise CnnArtifactIntegrityError("Registered CNN checkpoint is missing.")
    checkpoint_sha256 = _sha256(checkpoint)
    if checkpoint_sha256 != manifest.get("checkpoint_sha256"):
        raise CnnArtifactIntegrityError("Registered CNN checkpoint checksum does not match.")
    checkpoint_bytes = checkpoint.stat().st_size
    if checkpoint_bytes != manifest.get("checkpoint_bytes"):
        raise CnnArtifactIntegrityError("Registered CNN checkpoint size does not match.")

    model_data = manifest.get("model_configuration")
    training_data = manifest.get("training_configuration")
    if not isinstance(model_data, dict) or not isinstance(training_data, dict):
        raise CnnArtifactIntegrityError("CNN manifest configuration is invalid.")
    if history.get("configuration") != training_data:
        raise CnnArtifactIntegrityError("CNN history configuration does not match.")

    model = FashionCnn(ModelConfiguration(**model_data))
    try:
        payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
        if payload["model_configuration"] != model_data:
            raise CnnArtifactIntegrityError("CNN checkpoint model contract does not match.")
        if payload["training_configuration"] != training_data:
            raise CnnArtifactIntegrityError("CNN checkpoint training contract does not match.")
        if payload["dataset_version"] != DATASET_VERSION:
            raise CnnArtifactIntegrityError("CNN checkpoint dataset contract does not match.")
        model.load_state_dict(payload["model_state_dict"], strict=True)
    except (OSError, KeyError, RuntimeError, TypeError) as exc:
        raise CnnArtifactIntegrityError("Registered CNN checkpoint cannot be loaded.") from exc
    model.eval()

    sample_gallery_sha256 = manifest.get("sample_gallery_sha256")
    if not isinstance(sample_gallery_sha256, str):
        raise CnnArtifactIntegrityError("CNN sample gallery checksum is missing.")
    samples = _validated_samples(
        samples_document,
        sample_gallery_sha256,
        samples_path,
    )
    return CnnArtifactBundle(
        model=model,
        manifest=manifest,
        history=history,
        samples=samples,
        checkpoint_sha256=checkpoint_sha256,
        checkpoint_bytes=checkpoint_bytes,
    )
