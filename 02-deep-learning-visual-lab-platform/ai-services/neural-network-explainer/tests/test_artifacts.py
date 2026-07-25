from __future__ import annotations

from pathlib import Path

import pytest
from neural_network_explainer import artifacts
from neural_network_explainer.artifacts import ArtifactIntegrityError, load_artifact_bundle


def test_registered_bundle_loads_with_verified_evidence(
    artifact_directory: Path,
) -> None:
    bundle = load_artifact_bundle(artifact_directory)
    assert bundle.model.parameter_count == 17
    assert bundle.manifest["metrics"]["accuracy"] == 1.0
    assert len(bundle.checkpoint_sha256) == 64


def test_corrupted_checkpoint_is_rejected(
    artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(artifacts, "_sha256", lambda _: "0" * 64)
    with pytest.raises(ArtifactIntegrityError, match="checksum"):
        load_artifact_bundle(artifact_directory)


def test_mismatched_history_is_rejected(
    artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_read_json = artifacts._read_json

    def mismatched_history(path: Path) -> dict[str, object]:
        value = original_read_json(path)
        if path.name == "training-history.json":
            return {**value, "model_version": "not-registered"}
        return value

    monkeypatch.setattr(artifacts, "_read_json", mismatched_history)
    with pytest.raises(ArtifactIntegrityError, match="history"):
        load_artifact_bundle(artifact_directory)
