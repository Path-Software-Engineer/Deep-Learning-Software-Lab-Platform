from __future__ import annotations

from app.main import app
from fastapi.testclient import TestClient


def test_registered_artifact_drives_the_full_sprint_one_flow() -> None:
    with TestClient(app) as client:
        summary = client.get("/api/v1/neural-network/summary").json()
        history = client.get("/api/v1/neural-network/training-history").json()
        trace = client.post(
            "/api/v1/neural-network/forward",
            json={"inputs": [1, 0]},
        ).json()
    assert summary["model_version"] == "xor-mlp-v1"
    assert history["model_version"] == summary["model_version"]
    assert trace["checkpoint_sha256"] == summary["checkpoint"]["sha256"]
    assert trace["prediction"] == 1
    assert history["metrics"]["accuracy"] == 1.0
