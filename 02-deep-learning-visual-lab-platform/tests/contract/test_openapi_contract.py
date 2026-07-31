from __future__ import annotations

from app.main import app


def test_openapi_contains_all_published_platform_business_routes() -> None:
    paths = app.openapi()["paths"]
    assert {
        "/health",
        "/api/v1/platform/modules",
        "/api/v1/neural-network/summary",
        "/api/v1/neural-network/forward",
        "/api/v1/neural-network/training-history",
        "/api/v1/cnn/summary",
        "/api/v1/cnn/samples",
        "/api/v1/cnn/predict",
        "/api/v1/cnn/feature-maps",
        "/api/v1/autoencoder/summary",
        "/api/v1/autoencoder/samples",
        "/api/v1/autoencoder/reconstruct",
        "/api/v1/autoencoder/latent-points",
        "/api/v1/autoencoder/interpolate",
    }.issubset(paths)
    forbidden = {
        "/api/v1/neural-network/catalog",
        "/api/v1/neural-network/experiment",
        "/api/v1/neural-network/experiment/reset",
        "/api/v1/neural-network/experiment/train",
    }
    assert forbidden.isdisjoint(paths)
    assert paths["/api/v1/neural-network/forward"]["post"]["requestBody"]["required"] is True


def test_forward_response_contract_references_typed_resources() -> None:
    operation = app.openapi()["paths"]["/api/v1/neural-network/forward"]["post"]
    success_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    error_schema = operation["responses"]["422"]["content"]["application/json"]["schema"]
    assert success_schema["$ref"].endswith("/ForwardResource")
    assert error_schema["$ref"].endswith("/ErrorEnvelope")


def test_feature_map_response_contract_references_typed_resources() -> None:
    operation = app.openapi()["paths"]["/api/v1/cnn/feature-maps"]["post"]
    success_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    error_schema = operation["responses"]["422"]["content"]["application/json"]["schema"]
    assert success_schema["$ref"].endswith("/CnnFeatureMapsResource")
    assert error_schema["$ref"].endswith("/ErrorEnvelope")


def test_autoencoder_write_contracts_reference_typed_resources() -> None:
    paths = app.openapi()["paths"]
    reconstruction = paths["/api/v1/autoencoder/reconstruct"]["post"]
    interpolation = paths["/api/v1/autoencoder/interpolate"]["post"]

    assert reconstruction["requestBody"]["required"] is True
    assert reconstruction["responses"]["200"]["content"]["application/json"][
        "schema"
    ]["$ref"].endswith("/AutoencoderReconstructionResource")
    assert interpolation["requestBody"]["required"] is True
    assert interpolation["responses"]["200"]["content"]["application/json"][
        "schema"
    ]["$ref"].endswith("/AutoencoderInterpolationResource")
