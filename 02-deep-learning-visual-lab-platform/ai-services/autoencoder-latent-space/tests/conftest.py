from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def autoencoder_artifact_directory() -> Path:
    return Path(__file__).resolve().parents[3] / "models" / "autoencoder"
