"""Read-only platform catalog endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from app.common.resources import ModuleResource, ModulesResource

router = APIRouter(prefix="/platform", tags=["Platform"])


@router.get(
    "/modules",
    response_model=ModulesResource,
    summary="List the modules implemented in the current platform increment",
)
def list_modules() -> ModulesResource:
    return ModulesResource(
        modules=[
            ModuleResource(
                id="neural-network-explainer",
                name="Neural Network Explainer",
                description="Inspect a registered PyTorch MLP and its forward trace.",
                path="/",
                status="available",
                sprint=1,
            ),
            ModuleResource(
                id="cnn-feature-map-viewer",
                name="CNN Feature Map Viewer",
                description="Classify Fashion-MNIST images and inspect allowlisted feature maps.",
                path="/cnn",
                status="available",
                sprint=2,
            ),
        ]
    )
