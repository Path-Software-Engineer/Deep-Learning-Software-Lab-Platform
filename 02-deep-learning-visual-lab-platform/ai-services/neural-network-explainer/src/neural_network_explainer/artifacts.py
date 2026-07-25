"""Load and validate the registered PyTorch model and its evidence."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import torch

from neural_network_explainer.config import MODEL_VERSION, ModelConfiguration
from neural_network_explainer.model import ExplainableXorMlp


class ArtifactIntegrityError(RuntimeError):
    """Raised when registered model evidence is incomplete or inconsistent."""


@dataclass(frozen=True, slots=True)
class ArtifactBundle:
    model: ExplainableXorMlp
    manifest: dict[str, Any]
    history: dict[str, Any]
    checkpoint_sha256: str
    checkpoint_bytes: int


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactIntegrityError(f"Cannot read registered artifact: {path.name}") from exc
    if not isinstance(value, dict):
        raise ArtifactIntegrityError(f"Registered artifact must be an object: {path.name}")
    return cast(dict[str, Any], value)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(64 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ArtifactIntegrityError(f"Cannot read registered checkpoint: {path.name}") from exc
    return digest.hexdigest()


def load_artifact_bundle(directory: Path) -> ArtifactBundle:
    manifest = _read_json(directory / "manifest.json")
    history = _read_json(directory / "training-history.json")
    if manifest.get("model_version") != MODEL_VERSION:
        raise ArtifactIntegrityError("Manifest model version is not registered.")
    if history.get("model_version") != MODEL_VERSION:
        raise ArtifactIntegrityError("Training history does not match the registered model.")

    checkpoint = directory / str(manifest.get("checkpoint", ""))
    if not checkpoint.is_file():
        raise ArtifactIntegrityError("Registered checkpoint is missing.")
    checkpoint_sha256 = _sha256(checkpoint)
    if checkpoint_sha256 != manifest.get("checkpoint_sha256"):
        raise ArtifactIntegrityError("Registered checkpoint checksum does not match.")
    checkpoint_bytes = checkpoint.stat().st_size
    if checkpoint_bytes != manifest.get("checkpoint_bytes"):
        raise ArtifactIntegrityError("Registered checkpoint size does not match.")

    model_data = manifest.get("model_configuration")
    if not isinstance(model_data, dict):
        raise ArtifactIntegrityError("Manifest model configuration is invalid.")
    training_data = manifest.get("training_configuration")
    if not isinstance(training_data, dict):
        raise ArtifactIntegrityError("Manifest training configuration is invalid.")
    if history.get("configuration") != training_data:
        raise ArtifactIntegrityError("Training history configuration does not match the manifest.")
    if history.get("seed") != training_data.get("seed"):
        raise ArtifactIntegrityError("Training history seed does not match the manifest.")

    manifest_metrics = manifest.get("metrics")
    history_metrics = history.get("metrics")
    if not isinstance(manifest_metrics, dict) or not isinstance(history_metrics, dict):
        raise ArtifactIntegrityError("Registered training metrics are invalid.")
    for metric in ("accuracy", "final_loss"):
        if history_metrics.get(metric) != manifest_metrics.get(metric):
            raise ArtifactIntegrityError("Training history metrics do not match the manifest.")

    configuration = ModelConfiguration(**model_data)
    model = ExplainableXorMlp(configuration)
    try:
        payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
        if payload["model_configuration"] != model_data:
            raise ArtifactIntegrityError(
                "Checkpoint model configuration does not match the manifest."
            )
        if payload["training_configuration"] != training_data:
            raise ArtifactIntegrityError(
                "Checkpoint training configuration does not match the manifest."
            )
        model.load_state_dict(payload["model_state_dict"], strict=True)
    except (OSError, KeyError, RuntimeError, TypeError) as exc:
        raise ArtifactIntegrityError("Registered checkpoint cannot be loaded.") from exc
    model.eval()

    return ArtifactBundle(
        model=model,
        manifest=manifest,
        history=history,
        checkpoint_sha256=checkpoint_sha256,
        checkpoint_bytes=checkpoint_bytes,
    )
