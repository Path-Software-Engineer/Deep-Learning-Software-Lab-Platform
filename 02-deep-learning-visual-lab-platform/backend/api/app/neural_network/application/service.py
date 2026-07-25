"""Use-case boundary between HTTP resources and the PyTorch service."""

from __future__ import annotations

from neural_network_explainer.service import NeuralNetworkExplainer

from app.neural_network.interfaces.resources import (
    ForwardResource,
    NeuralNetworkSummaryResource,
    TrainingHistoryResource,
)


class NeuralNetworkApplicationService:
    def __init__(self, explainer: NeuralNetworkExplainer) -> None:
        self._explainer = explainer

    def get_summary(self) -> NeuralNetworkSummaryResource:
        return NeuralNetworkSummaryResource.model_validate(self._explainer.summary())

    def execute_forward(self, inputs: tuple[float, float]) -> ForwardResource:
        return ForwardResource.model_validate(self._explainer.forward(inputs))

    def get_training_history(self) -> TrainingHistoryResource:
        return TrainingHistoryResource.model_validate(self._explainer.training_history())
