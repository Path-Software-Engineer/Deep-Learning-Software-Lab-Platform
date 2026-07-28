"""FastAPI composition root for the first two platform increments."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from cnn_feature_map_viewer import CnnArtifactIntegrityError, CnnRequestError
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from neural_network_explainer import ArtifactIntegrityError

from app.cnn.interfaces.router import router as cnn_router
from app.common.resources import (
    ErrorEnvelope,
    ErrorItemResource,
    ErrorResource,
    HealthResource,
    validation_details,
)
from app.core.settings import settings
from app.main_dependencies import cnn_service, neural_network_service
from app.neural_network.interfaces.router import router as neural_network_router
from app.platform.interfaces.router import router as platform_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    neural_network_service.get_summary()
    cnn_service.get_summary()
    yield


app = FastAPI(
    title=settings.title,
    description=(
        "Typed read and forward-pass API for the educational Deep Learning Visual Lab. "
        "Training is intentionally offline."
    ),
    version=settings.version,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(platform_router, prefix=settings.api_prefix)
app.include_router(neural_network_router, prefix=settings.api_prefix)
app.include_router(cnn_router, prefix=settings.api_prefix)


@app.exception_handler(RequestValidationError)
async def request_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorResource(
            code="validation_error",
            message="The request does not match the published API contract.",
            details=validation_details(exc.errors()),
        )
    )
    return JSONResponse(status_code=422, content=envelope.model_dump())


@app.exception_handler(ValueError)
async def domain_validation_error(_: Request, exc: ValueError) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorResource(code="invalid_xor_input", message=str(exc))
    )
    return JSONResponse(status_code=422, content=envelope.model_dump())


@app.exception_handler(CnnRequestError)
async def cnn_request_error(_: Request, exc: CnnRequestError) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorResource(
            code=exc.code,
            message=str(exc),
            details=[ErrorItemResource(field=exc.field, message=str(exc))],
        )
    )
    return JSONResponse(status_code=422, content=envelope.model_dump())


@app.exception_handler(ArtifactIntegrityError)
async def artifact_error(_: Request, exc: ArtifactIntegrityError) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorResource(code="artifact_unavailable", message=str(exc))
    )
    return JSONResponse(status_code=503, content=envelope.model_dump())


@app.exception_handler(CnnArtifactIntegrityError)
async def cnn_artifact_error(
    _: Request,
    exc: CnnArtifactIntegrityError,
) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorResource(code="cnn_artifact_unavailable", message=str(exc))
    )
    return JSONResponse(status_code=503, content=envelope.model_dump())


@app.get("/health", response_model=HealthResource, tags=["Health"])
def health() -> HealthResource:
    summary = neural_network_service.get_summary()
    cnn_summary = cnn_service.get_summary()
    return HealthResource(
        status="ok",
        service="deep-learning-visual-lab-api",
        version=settings.version,
        artifact=f"{summary.model_version}|{cnn_summary.model.version}",
    )
