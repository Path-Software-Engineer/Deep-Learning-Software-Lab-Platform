from __future__ import annotations

from pathlib import Path

import pytest
from cnn_feature_map_viewer import artifacts
from cnn_feature_map_viewer.artifacts import (
    CnnArtifactIntegrityError,
    load_cnn_artifact_bundle,
)


def test_registered_cnn_bundle_loads(cnn_artifact_directory: Path) -> None:
    bundle = load_cnn_artifact_bundle(cnn_artifact_directory)

    assert bundle.model.parameter_count == 207_018
    assert bundle.checkpoint_bytes > 0
    assert len(bundle.checkpoint_sha256) == 64
    assert len(bundle.samples) == 10


def test_checkpoint_checksum_mismatch_fails_closed(
    cnn_artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = artifacts._sha256

    def mismatched_checkpoint(path: Path) -> str:
        return "0" * 64 if path.suffix == ".pt" else original_sha256(path)

    monkeypatch.setattr(artifacts, "_sha256", mismatched_checkpoint)

    with pytest.raises(CnnArtifactIntegrityError, match="checkpoint checksum"):
        load_cnn_artifact_bundle(cnn_artifact_directory)


def test_sample_gallery_checksum_mismatch_fails_closed(
    cnn_artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = artifacts._sha256

    def mismatched_gallery(path: Path) -> str:
        return "0" * 64 if path.name == "sample-gallery.json" else original_sha256(path)

    monkeypatch.setattr(artifacts, "_sha256", mismatched_gallery)

    with pytest.raises(CnnArtifactIntegrityError, match="gallery checksum"):
        load_cnn_artifact_bundle(cnn_artifact_directory)
