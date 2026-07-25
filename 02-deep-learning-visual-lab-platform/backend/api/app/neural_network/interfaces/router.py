"""Thin HTTP interface for the Neural Network Explainer use cases."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.common.resources import ErrorEnvelope
from app.main_dependencies import get_neural_network_service
from app.neural_network.application.service import NeuralNetworkApplicationService
from app.neural_network.interfaces.resources import (
    ForwardRequest,
    ForwardResource,
    NeuralNetworkSummaryResource,
    TrainingHistoryResource,
)

router = APIRouter(prefix="/neural-network", tags=["Neural Network Explainer"])
Service = Annotated[NeuralNetworkApplicationService, Depends(get_neural_network_service)]


@router.get("/summary", response_model=NeuralNetworkSummaryResource)
def get_summary(service: Service) -> NeuralNetworkSummaryResource:
    return service.get_summary()


@router.post(
    "/forward",
    response_model=ForwardResource,
    responses={422: {"model": ErrorEnvelope}},
)
def execute_forward(
    request: Annotated[ForwardRequest, Body()],
    service: Service,
) -> ForwardResource:
    return service.execute_forward(request.inputs)


@router.get("/training-history", response_model=TrainingHistoryResource)
def get_training_history(service: Service) -> TrainingHistoryResource:
    return service.get_training_history()
