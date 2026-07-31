"""Application-neutral reconstruction, neighborhood and interpolation services."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import torch
from torch import nn

from autoencoder_latent_space.artifacts import (
    load_autoencoder_artifact_bundle,
)
from autoencoder_latent_space.config import (
    CLASS_NAMES,
    DATASET_VERSION,
    LIMITATIONS,
    MAX_INTERPOLATION_STEPS,
    MIN_INTERPOLATION_STEPS,
    MODEL_VERSION,
    MODULE_ID,
    NEIGHBOR_COUNT,
    PREPROCESSING_CONFIGURATION,
    SCHEMA_VERSION,
)
from autoencoder_latent_space.dataset import dataset_metadata
from autoencoder_latent_space.image_utils import pixels_to_data_uri


class AutoencoderRequestError(ValueError):
    def __init__(self, code: str, message: str, field: str) -> None:
        super().__init__(message)
        self.code = code
        self.field = field


def _pixels(point: dict[str, Any]) -> torch.Tensor:
    return (
        torch.tensor(point["pixels"], dtype=torch.float32)
        .div(255.0)
        .unsqueeze(0)
    )


def _coordinate(point: dict[str, Any]) -> torch.Tensor:
    return torch.tensor(point["coordinate"], dtype=torch.float32)


class AutoencoderLatentSpace:
    """Read-only boundary around one integrity-checked autoencoder bundle."""

    def __init__(self, artifact_directory: Path) -> None:
        self._bundle = load_autoencoder_artifact_bundle(artifact_directory)
        self._points_by_id = {
            str(point["id"]): point for point in self._bundle.points
        }

    def _point(self, point_id: str) -> dict[str, Any]:
        point = self._points_by_id.get(point_id)
        if point is None:
            raise AutoencoderRequestError(
                "unknown_latent_point",
                "The requested latent point is not part of the registered gallery.",
                "point_id",
            )
        return point

    @staticmethod
    def _point_summary(point: dict[str, Any]) -> dict[str, Any]:
        pixels = _pixels(point)
        return {
            "id": point["id"],
            "source_index": point["source_index"],
            "label_index": point["label_index"],
            "label": CLASS_NAMES[int(point["label_index"])],
            "coordinate": point["coordinate"],
            "reconstruction_error": point["reconstruction_error"],
            "image_data_uri": pixels_to_data_uri(pixels),
        }

    def summary(self) -> dict[str, Any]:
        manifest = self._bundle.manifest
        model_configuration = manifest["model_configuration"]
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "status": "available",
            "model": {
                "name": "Fashion convolutional autoencoder",
                "version": MODEL_VERSION,
                "framework": manifest["framework"],
                "architecture": (
                    "Conv(16, stride 2) → Conv(32, stride 2) → Dense(64) → "
                    "Latent(2) → Dense(64) → ConvTranspose(16) → ConvTranspose(1)"
                ),
                "parameter_count": self._bundle.model.parameter_count,
                "input_shape": [1, 28, 28],
                "latent_shape": [model_configuration["latent_dimensions"]],
                "output_shape": [1, 28, 28],
                "dataset": DATASET_VERSION,
                "checkpoint": {
                    "file": manifest["checkpoint"],
                    "sha256": self._bundle.checkpoint_sha256,
                    "bytes": self._bundle.checkpoint_bytes,
                },
            },
            "dataset": dataset_metadata(),
            "preprocessing": asdict(PREPROCESSING_CONFIGURATION),
            "evaluation": manifest["evaluation"],
            "latent_contract": {
                "dimensions": 2,
                "distance": "euclidean-in-registered-2d-bottleneck",
                "bounds": manifest["latent_bounds"],
                "reference_points": len(self._bundle.points),
                "neighbors_returned": NEIGHBOR_COUNT,
                "interpolation": "linear-coordinate-segment-decoded-by-registered-model",
                "minimum_steps": MIN_INTERPOLATION_STEPS,
                "maximum_steps": MAX_INTERPOLATION_STEPS,
            },
            "limitations": list(LIMITATIONS),
        }

    def samples(self) -> dict[str, Any]:
        representatives: list[dict[str, Any]] = []
        for label_index in range(len(CLASS_NAMES)):
            candidates = [
                point
                for point in self._bundle.points
                if point["label_index"] == label_index
            ]
            selected = min(
                candidates,
                key=lambda point: float(point["reconstruction_error"]),
            )
            representatives.append(self._point_summary(selected))
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "samples": representatives,
        }

    def latent_points(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "model_version": MODEL_VERSION,
            "bounds": self._bundle.manifest["latent_bounds"],
            "points": [
                self._point_summary(point) for point in self._bundle.points
            ],
            "interpretation": (
                "Coordinates and distances belong only to this registered "
                "two-dimensional bottleneck."
            ),
        }

    def _neighbors(
        self,
        point: dict[str, Any],
    ) -> list[dict[str, Any]]:
        origin = _coordinate(point)
        candidates: list[tuple[float, dict[str, Any]]] = []
        for candidate in self._bundle.points:
            if candidate["id"] == point["id"]:
                continue
            distance = float(torch.linalg.vector_norm(_coordinate(candidate) - origin))
            candidates.append((distance, candidate))
        candidates.sort(key=lambda value: (value[0], str(value[1]["id"])))
        return [
            {
                **self._point_summary(candidate),
                "distance": distance,
            }
            for distance, candidate in candidates[:NEIGHBOR_COUNT]
        ]

    def reconstruct(self, point_id: str) -> dict[str, Any]:
        point = self._point(point_id)
        inputs = _pixels(point).unsqueeze(0)
        self._bundle.model.eval()
        with torch.inference_mode():
            reconstruction, coordinates = self._bundle.model(inputs)
        error = float(nn.functional.mse_loss(reconstruction, inputs).item())
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "model_version": MODEL_VERSION,
            "sample": self._point_summary(point),
            "original": {
                "tensor_shape": list(inputs.shape),
                "image_data_uri": pixels_to_data_uri(inputs[0]),
            },
            "reconstruction": {
                "tensor_shape": list(reconstruction.shape),
                "image_data_uri": pixels_to_data_uri(reconstruction[0]),
                "mean_squared_error": error,
                "mean_absolute_error": float(
                    nn.functional.l1_loss(reconstruction, inputs).item()
                ),
            },
            "latent_coordinate": [
                round(float(value), 6) for value in coordinates[0].tolist()
            ],
            "neighbors": self._neighbors(point),
            "interpretation": (
                "The reconstruction and error were produced by the registered "
                "encoder-decoder. Neighbor order uses Euclidean latent distance."
            ),
        }

    def interpolate(
        self,
        *,
        start_id: str,
        end_id: str,
        steps: int,
    ) -> dict[str, Any]:
        if start_id == end_id:
            raise AutoencoderRequestError(
                "identical_interpolation_endpoints",
                "Choose two different registered latent points.",
                "end_id",
            )
        if not MIN_INTERPOLATION_STEPS <= steps <= MAX_INTERPOLATION_STEPS:
            raise AutoencoderRequestError(
                "invalid_interpolation_steps",
                (
                    f"Interpolation steps must be between "
                    f"{MIN_INTERPOLATION_STEPS} and {MAX_INTERPOLATION_STEPS}."
                ),
                "steps",
            )
        start = self._point(start_id)
        end = self._point(end_id)
        start_coordinate = _coordinate(start)
        end_coordinate = _coordinate(end)
        alphas = torch.linspace(0.0, 1.0, steps=steps)
        coordinates = torch.stack(
            [
                (1.0 - alpha) * start_coordinate + alpha * end_coordinate
                for alpha in alphas
            ]
        )
        self._bundle.model.eval()
        with torch.inference_mode():
            decoded = self._bundle.model.decode(coordinates)
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "model_version": MODEL_VERSION,
            "start": self._point_summary(start),
            "end": self._point_summary(end),
            "steps": [
                {
                    "index": index,
                    "alpha": float(alphas[index]),
                    "coordinate": [
                        round(float(value), 6)
                        for value in coordinates[index].tolist()
                    ],
                    "image_data_uri": pixels_to_data_uri(decoded[index]),
                }
                for index in range(steps)
            ],
            "interpretation": (
                "Every frame is decoded from a linear segment in this model's "
                "2D bottleneck. Smoothness is not evidence of causal understanding."
            ),
        }
