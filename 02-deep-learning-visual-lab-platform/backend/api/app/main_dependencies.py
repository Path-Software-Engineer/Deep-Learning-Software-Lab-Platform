"""Dependency providers kept outside the FastAPI composition root."""

from __future__ import annotations

from neural_network_explainer import NeuralNetworkExplainer

from app.core.settings import settings
from app.neural_network.application.service import NeuralNetworkApplicationService

neural_network_service = NeuralNetworkApplicationService(
    NeuralNetworkExplainer(settings.artifact_directory)
)


def get_neural_network_service() -> NeuralNetworkApplicationService:
    return neural_network_service
