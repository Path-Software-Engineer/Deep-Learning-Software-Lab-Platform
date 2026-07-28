"""Export the deterministic FastAPI OpenAPI contract for review and versioning."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend" / "api"))
sys.path.insert(
    0,
    str(
        PROJECT_ROOT
        / "ai-services"
        / "neural-network-explainer"
        / "src"
    ),
)
sys.path.insert(
    0,
    str(
        PROJECT_ROOT
        / "ai-services"
        / "cnn-feature-map-viewer"
        / "src"
    ),
)

from app.main import app  # noqa: E402


def main() -> None:
    destination = PROJECT_ROOT / "docs" / "api" / "openapi.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(app.openapi(), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Exported OpenAPI contract: {destination}")


if __name__ == "__main__":
    main()
