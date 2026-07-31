from __future__ import annotations

from pathlib import Path

import pytest
from autoencoder_latent_space import artifacts
from autoencoder_latent_space.artifacts import (
    AutoencoderArtifactIntegrityError,
    load_autoencoder_artifact_bundle,
)


def test_registered_autoencoder_bundle_loads(
    autoencoder_artifact_directory: Path,
) -> None:
    bundle = load_autoencoder_artifact_bundle(autoencoder_artifact_directory)

    assert bundle.model.parameter_count == 215_923
    assert bundle.checkpoint_bytes > 0
    assert len(bundle.checkpoint_sha256) == 64
    assert len(bundle.points) == 100


def test_checkpoint_checksum_mismatch_fails_closed(
    autoencoder_artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = artifacts._sha256

    def mismatched_checkpoint(path: Path) -> str:
        return "0" * 64 if path.suffix == ".pt" else original_sha256(path)

    monkeypatch.setattr(artifacts, "_sha256", mismatched_checkpoint)
    with pytest.raises(
        AutoencoderArtifactIntegrityError,
        match="checkpoint checksum",
    ):
        load_autoencoder_artifact_bundle(autoencoder_artifact_directory)


def test_latent_gallery_checksum_mismatch_fails_closed(
    autoencoder_artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = artifacts._sha256

    def mismatched_gallery(path: Path) -> str:
        return "0" * 64 if path.name == "latent-gallery.json" else original_sha256(path)

    monkeypatch.setattr(artifacts, "_sha256", mismatched_gallery)
    with pytest.raises(
        AutoencoderArtifactIntegrityError,
        match="gallery checksum",
    ):
        load_autoencoder_artifact_bundle(autoencoder_artifact_directory)
