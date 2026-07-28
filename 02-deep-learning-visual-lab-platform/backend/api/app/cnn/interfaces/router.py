"""Thin FastAPI interface for CNN prediction and representation use cases."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.cnn.application.service import CnnApplicationService
from app.cnn.interfaces.resources import (
    CnnFeatureMapsResource,
    CnnPredictionResource,
    CnnSamplesResource,
    CnnSummaryResource,
)
from app.common.resources import ErrorEnvelope
from app.main_dependencies import get_cnn_service

router = APIRouter(prefix="/cnn", tags=["CNN Feature Map Viewer"])
Service = Annotated[CnnApplicationService, Depends(get_cnn_service)]

IMAGE_REQUEST_BODY = {
    "requestBody": {
        "required": False,
        "content": {
            "image/png": {"schema": {"type": "string", "format": "binary"}},
            "image/jpeg": {"schema": {"type": "string", "format": "binary"}},
        },
    }
}


async def _image_input(request: Request) -> tuple[bytes | None, str | None]:
    payload = await request.body()
    return (payload or None), request.headers.get("content-type")


@router.get("/summary", response_model=CnnSummaryResource)
def get_summary(service: Service) -> CnnSummaryResource:
    return service.get_summary()


@router.get("/samples", response_model=CnnSamplesResource)
def get_samples(service: Service) -> CnnSamplesResource:
    return service.get_samples()


@router.post(
    "/predict",
    response_model=CnnPredictionResource,
    responses={422: {"model": ErrorEnvelope}},
    openapi_extra=IMAGE_REQUEST_BODY,
)
async def predict(
    request: Request,
    service: Service,
    sample_id: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
) -> CnnPredictionResource:
    image_bytes, media_type = await _image_input(request)
    return service.predict(
        sample_id=sample_id,
        image_bytes=image_bytes,
        media_type=media_type,
    )


@router.post(
    "/feature-maps",
    response_model=CnnFeatureMapsResource,
    responses={422: {"model": ErrorEnvelope}},
    openapi_extra=IMAGE_REQUEST_BODY,
)
async def get_feature_maps(
    request: Request,
    service: Service,
    layer: Annotated[str, Query(min_length=1, max_length=64)],
    channels: Annotated[list[int], Query(min_length=1, max_length=12)],
    sample_id: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
) -> CnnFeatureMapsResource:
    image_bytes, media_type = await _image_input(request)
    return service.get_feature_maps(
        sample_id=sample_id,
        image_bytes=image_bytes,
        media_type=media_type,
        layer=layer,
        channels=tuple(channels),
    )
