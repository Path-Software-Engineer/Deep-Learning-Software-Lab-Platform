"""Thin FastAPI interface for autoencoder representation use cases."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.autoencoder.application.service import AutoencoderApplicationService
from app.autoencoder.interfaces.resources import (
    AutoencoderInterpolationRequest,
    AutoencoderInterpolationResource,
    AutoencoderLatentPointsResource,
    AutoencoderReconstructionResource,
    AutoencoderReconstructRequest,
    AutoencoderSamplesResource,
    AutoencoderSummaryResource,
)
from app.common.resources import ErrorEnvelope
from app.main_dependencies import get_autoencoder_service

router = APIRouter(
    prefix="/autoencoder",
    tags=["Autoencoder Latent Space Demo"],
)
Service = Annotated[
    AutoencoderApplicationService,
    Depends(get_autoencoder_service),
]


@router.get("/summary", response_model=AutoencoderSummaryResource)
def get_summary(service: Service) -> AutoencoderSummaryResource:
    return service.get_summary()


@router.get("/samples", response_model=AutoencoderSamplesResource)
def get_samples(service: Service) -> AutoencoderSamplesResource:
    return service.get_samples()


@router.get("/latent-points", response_model=AutoencoderLatentPointsResource)
def get_latent_points(service: Service) -> AutoencoderLatentPointsResource:
    return service.get_latent_points()


@router.post(
    "/reconstruct",
    response_model=AutoencoderReconstructionResource,
    responses={422: {"model": ErrorEnvelope}},
)
def reconstruct(
    request: AutoencoderReconstructRequest,
    service: Service,
) -> AutoencoderReconstructionResource:
    return service.reconstruct(request.point_id)


@router.post(
    "/interpolate",
    response_model=AutoencoderInterpolationResource,
    responses={422: {"model": ErrorEnvelope}},
)
def interpolate(
    request: AutoencoderInterpolationRequest,
    service: Service,
) -> AutoencoderInterpolationResource:
    return service.interpolate(
        start_id=request.start_id,
        end_id=request.end_id,
        steps=request.steps,
    )
