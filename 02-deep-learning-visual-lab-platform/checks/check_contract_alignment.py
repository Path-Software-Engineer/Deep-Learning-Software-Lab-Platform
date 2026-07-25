"""Validate exported OpenAPI routes against the frontend API client."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUSINESS_ROUTES = {
    "/api/v1/platform/modules": "get",
    "/api/v1/neural-network/summary": "get",
    "/api/v1/neural-network/forward": "post",
    "/api/v1/neural-network/training-history": "get",
}
FORBIDDEN_ROUTES = {
    "/api/v1/neural-network/catalog",
    "/api/v1/neural-network/experiment",
    "/api/v1/neural-network/experiment/reset",
    "/api/v1/neural-network/experiment/train",
}


def main() -> None:
    schema = json.loads(
        (PROJECT_ROOT / "docs" / "api" / "openapi.json").read_text(encoding="utf-8")
    )
    paths = schema["paths"]
    for path, method in BUSINESS_ROUTES.items():
        assert method in paths.get(path, {}), f"OpenAPI is missing {method.upper()} {path}"
    for path in FORBIDDEN_ROUTES:
        assert path not in paths, f"OpenAPI exposes a route outside the Sprint 1 contract: {path}"

    api_client = (
        PROJECT_ROOT / "frontend" / "lab-app" / "lib" / "api-client.ts"
    ).read_text(encoding="utf-8")
    for path in BUSINESS_ROUTES:
        if path != "/api/v1/platform/modules":
            assert path in api_client, f"frontend client is missing {path}"
    for path in FORBIDDEN_ROUTES:
        assert path not in api_client, f"frontend client references unsupported route {path}"

    print("OK - Sprint 1 OpenAPI/frontend contract alignment passed")
    print("Routes: platform modules, model summary, forward trace and training history")


if __name__ == "__main__":
    main()
