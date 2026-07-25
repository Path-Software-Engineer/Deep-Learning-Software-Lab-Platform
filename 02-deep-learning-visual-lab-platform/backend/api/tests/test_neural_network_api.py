from __future__ import annotations

from fastapi.testclient import TestClient


def test_summary_exposes_the_registered_model(client: TestClient) -> None:
    response = client.get("/api/v1/neural-network/summary")
    assert response.status_code == 200
    resource = response.json()
    assert resource["engine"] == "PyTorch"
    assert resource["architecture"]["parameter_count"] == 17
    assert resource["checkpoint"]["sha256"]


def test_forward_returns_real_layer_values(client: TestClient) -> None:
    response = client.post("/api/v1/neural-network/forward", json={"inputs": [0, 1]})
    assert response.status_code == 200
    resource = response.json()
    assert resource["prediction"] == 1
    assert resource["target"] == 1
    assert [layer["id"] for layer in resource["layers"]] == ["hidden", "output"]
    assert len(resource["layers"][0]["activations"]) == 4


def test_training_history_is_read_only_registered_evidence(client: TestClient) -> None:
    response = client.get("/api/v1/neural-network/training-history")
    assert response.status_code == 200
    resource = response.json()
    assert resource["configuration"]["optimizer"] == "Adam"
    assert resource["metrics"]["accuracy"] == 1.0
    assert resource["points"][-1]["epoch"] == 2000


def test_non_binary_input_has_a_typed_validation_error(client: TestClient) -> None:
    response = client.post("/api/v1/neural-network/forward", json={"inputs": [0.5, 1]})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["details"][0]["field"] == "inputs"


def test_unknown_fields_and_missing_inputs_are_rejected(client: TestClient) -> None:
    unknown = client.post(
        "/api/v1/neural-network/forward",
        json={"inputs": [0, 1], "epochs": 100},
    )
    missing = client.post("/api/v1/neural-network/forward", json={})
    assert unknown.status_code == 422
    assert missing.status_code == 422
