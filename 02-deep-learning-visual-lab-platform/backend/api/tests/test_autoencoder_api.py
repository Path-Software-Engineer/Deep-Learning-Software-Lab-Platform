from __future__ import annotations

from fastapi.testclient import TestClient


def test_autoencoder_summary_samples_and_points_are_published(
    client: TestClient,
) -> None:
    summary = client.get("/api/v1/autoencoder/summary")
    samples = client.get("/api/v1/autoencoder/samples")
    points = client.get("/api/v1/autoencoder/latent-points")

    assert summary.status_code == 200
    assert summary.json()["model"]["version"] == "fashion-autoencoder-2d-v1"
    assert summary.json()["evaluation"]["samples"] == 150
    assert summary.json()["latent_contract"]["dimensions"] == 2
    assert samples.status_code == 200
    assert len(samples.json()["samples"]) == 10
    assert points.status_code == 200
    assert len(points.json()["points"]) == 100


def test_reconstruction_contract_includes_real_error_and_neighbors(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/autoencoder/reconstruct",
        json={"point_id": "latent-08-00"},
    )

    assert response.status_code == 200
    resource = response.json()
    assert resource["sample"]["label"] == "Bag"
    assert resource["reconstruction"]["mean_squared_error"] >= 0
    assert resource["reconstruction"]["image_data_uri"].startswith(
        "data:image/png;base64,"
    )
    assert len(resource["latent_coordinate"]) == 2
    assert len(resource["neighbors"]) == 5


def test_interpolation_contract_decodes_requested_sequence(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/autoencoder/interpolate",
        json={
            "start_id": "latent-01-00",
            "end_id": "latent-09-00",
            "steps": 7,
        },
    )

    assert response.status_code == 200
    resource = response.json()
    assert len(resource["steps"]) == 7
    assert resource["steps"][0]["alpha"] == 0.0
    assert resource["steps"][-1]["alpha"] == 1.0


def test_unknown_point_and_identical_endpoints_use_stable_errors(
    client: TestClient,
) -> None:
    unknown = client.post(
        "/api/v1/autoencoder/reconstruct",
        json={"point_id": "unknown"},
    )
    identical = client.post(
        "/api/v1/autoencoder/interpolate",
        json={
            "start_id": "latent-01-00",
            "end_id": "latent-01-00",
            "steps": 7,
        },
    )

    assert unknown.status_code == 422
    assert unknown.json()["error"]["code"] == "unknown_latent_point"
    assert identical.status_code == 422
    assert (
        identical.json()["error"]["code"]
        == "identical_interpolation_endpoints"
    )


def test_invalid_interpolation_payload_is_rejected_by_contract(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/autoencoder/interpolate",
        json={
            "start_id": "latent-01-00",
            "end_id": "latent-02-00",
            "steps": 99,
            "unexpected": True,
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
