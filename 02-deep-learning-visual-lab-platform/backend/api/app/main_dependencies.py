"""Dependency providers kept outside the FastAPI composition root."""

from __future__ import annotations

from cnn_feature_map_viewer import CnnFeatureMapViewer
from neural_network_explainer import NeuralNetworkExplainer

from app.cnn.application.service import CnnApplicationService
from app.core.settings import settings
from app.neural_network.application.service import NeuralNetworkApplicationService

neural_network_service = NeuralNetworkApplicationService(
    NeuralNetworkExplainer(settings.artifact_directory)
)
cnn_service = CnnApplicationService(
    CnnFeatureMapViewer(settings.cnn_artifact_directory)
)


def get_neural_network_service() -> NeuralNetworkApplicationService:
    return neural_network_service


def get_cnn_service() -> CnnApplicationService:
    return cnn_service
