"""Environment-backed settings with repository-safe defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True, slots=True)
class Settings:
    title: str = "Deep Learning Visual Lab API"
    version: str = "0.2.0"
    api_prefix: str = "/api/v1"
    artifact_directory: Path = PROJECT_ROOT / "models" / "neural-network"
    cnn_artifact_directory: Path = PROJECT_ROOT / "models" / "cnn"
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    )


settings = Settings()
