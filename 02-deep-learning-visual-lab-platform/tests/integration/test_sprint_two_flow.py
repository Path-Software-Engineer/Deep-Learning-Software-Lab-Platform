from __future__ import annotations

from app.main import app
from fastapi.testclient import TestClient


def test_registered_artifact_drives_the_full_sprint_two_flow() -> None:
    with TestClient(app) as client:
        summary = client.get("/api/v1/cnn/summary").json()
        samples = client.get("/api/v1/cnn/samples").json()
        result = client.post(
            "/api/v1/cnn/feature-maps"
            "?sample_id=fashion-08"
            "&layer=block1_relu"
            "&channels=0&channels=1",
        ).json()

    assert summary["model"]["version"] == "fashion-cnn-v1"
    assert summary["evaluation"]["correct"] == 122
    assert len(samples["samples"]) == 10
    assert result["model_version"] == summary["model"]["version"]
    assert result["input"]["registered_label"] == "Bag"
    assert result["prediction"]["predicted_class"] == "Bag"
    assert result["representation"]["activation_tensor_shape"] == [1, 16, 28, 28]
    assert [item["channel"] for item in result["representation"]["maps"]] == [0, 1]
    assert all(
        item["normalization"] == "per-channel-min-max-for-display"
        for item in result["representation"]["maps"]
    )
