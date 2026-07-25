from __future__ import annotations

from app.main import app


def test_openapi_contains_only_the_published_sprint_one_business_routes() -> None:
    paths = app.openapi()["paths"]
    assert {
        "/health",
        "/api/v1/platform/modules",
        "/api/v1/neural-network/summary",
        "/api/v1/neural-network/forward",
        "/api/v1/neural-network/training-history",
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
