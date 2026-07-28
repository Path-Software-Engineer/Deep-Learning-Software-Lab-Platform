"""Application-neutral CNN prediction and feature-map services."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import torch

from cnn_feature_map_viewer.artifacts import (
    CnnArtifactBundle,
    load_cnn_artifact_bundle,
)
from cnn_feature_map_viewer.config import (
    CLASS_NAMES,
    DATASET_VERSION,
    LAYER_METADATA,
    LIMITATIONS,
    MAX_CHANNELS_PER_REQUEST,
    MODEL_VERSION,
    MODULE_ID,
    PREPROCESSING_CONFIGURATION,
    SCHEMA_VERSION,
)
from cnn_feature_map_viewer.dataset import dataset_metadata, normalize
from cnn_feature_map_viewer.hooks import run_with_activations
from cnn_feature_map_viewer.image_io import decode_image, pixels_to_data_uri


class CnnRequestError(ValueError):
    def __init__(self, code: str, message: str, field: str) -> None:
        super().__init__(message)
        self.code = code
        self.field = field


def _matrix(tensor: torch.Tensor) -> list[list[float]]:
    return [[round(float(value), 6) for value in row] for row in tensor.tolist()]


def _sample_pixels(sample: dict[str, Any]) -> torch.Tensor:
    pixels = torch.tensor(sample["pixels"], dtype=torch.float32) / 255.0
    return pixels.unsqueeze(0)


def _normalized_map(
    layer: str,
    channel: int,
    activation: torch.Tensor,
) -> dict[str, Any]:
    channel_map = activation[0, channel]
    raw_min = float(channel_map.min())
    raw_max = float(channel_map.max())
    span = raw_max - raw_min
    normalized = (
        torch.zeros_like(channel_map)
        if span <= 1e-12
        else (channel_map - raw_min) / span
    )
    metadata = LAYER_METADATA[layer]
    return {
        "layer": layer,
        "layer_label": metadata["label"],
        "operation": metadata["operation"],
        "channel": channel,
        "tensor_shape": list(activation.shape),
        "map_shape": list(channel_map.shape),
        "raw_min": raw_min,
        "raw_max": raw_max,
        "raw_mean": float(channel_map.mean()),
        "raw_std": float(channel_map.std(unbiased=False)),
        "normalization": "per-channel-min-max-for-display",
        "display_scale": [0.0, 1.0],
        "values": _matrix(normalized),
    }


class CnnFeatureMapViewer:
    def __init__(self, artifact_directory: Path) -> None:
        self._bundle: CnnArtifactBundle = load_cnn_artifact_bundle(artifact_directory)
        self._samples = {str(sample["id"]): sample for sample in self._bundle.samples}

    def summary(self) -> dict[str, Any]:
        model = self._bundle.model
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "status": "available",
            "model": {
                "name": "Fashion CNN",
                "version": MODEL_VERSION,
                "framework": str(self._bundle.manifest["framework"]),
                "architecture": "Conv-BN-ReLU-Pool ×2 → Dense(128) → 10 classes",
                "parameter_count": model.parameter_count,
                "input_shape": [1, 28, 28],
                "output_shape": [len(CLASS_NAMES)],
                "dataset": DATASET_VERSION,
                "checkpoint": {
                    "file": str(self._bundle.manifest["checkpoint"]),
                    "sha256": self._bundle.checkpoint_sha256,
                    "bytes": self._bundle.checkpoint_bytes,
                },
            },
            "dataset": dataset_metadata(),
            "preprocessing": asdict(PREPROCESSING_CONFIGURATION),
            "layers": [
                {"id": layer_id, **metadata}
                for layer_id, metadata in LAYER_METADATA.items()
            ],
            "evaluation": self._bundle.manifest["evaluation"],
            "visual_contract": {
                "transport": "bounded-json-matrix",
                "normalization": "per-channel-min-max-for-display",
                "display_scale": [0.0, 1.0],
                "maximum_channels_per_request": MAX_CHANNELS_PER_REQUEST,
            },
            "limitations": list(LIMITATIONS),
        }

    def samples(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "samples": [
                {
                    "id": sample["id"],
                    "source_index": sample["source_index"],
                    "label_index": sample["label_index"],
                    "label": CLASS_NAMES[int(sample["label_index"])],
                    "image_data_uri": pixels_to_data_uri(_sample_pixels(sample)),
                }
                for sample in self._bundle.samples
            ],
        }

    def _resolve_input(
        self,
        *,
        sample_id: str | None,
        image_bytes: bytes | None,
        media_type: str | None,
    ) -> tuple[torch.Tensor, dict[str, Any]]:
        if sample_id and image_bytes:
            raise CnnRequestError(
                "ambiguous_input",
                "Provide either a registered sample or an uploaded image, not both.",
                "input",
            )
        if sample_id:
            sample = self._samples.get(sample_id)
            if sample is None:
                raise CnnRequestError(
                    "invalid_sample",
                    "The requested sample is not part of the published allowlist.",
                    "sample_id",
                )
            pixels = _sample_pixels(sample)
            return normalize(pixels).unsqueeze(0), {
                "source": "registered-sample",
                "sample_id": sample_id,
                "source_index": sample["source_index"],
                "registered_label": CLASS_NAMES[int(sample["label_index"])],
                "original_shape": [28, 28],
                "tensor_shape": [1, 1, 28, 28],
                "preprocessing": asdict(PREPROCESSING_CONFIGURATION),
                "image_data_uri": pixels_to_data_uri(pixels),
            }
        if image_bytes is not None:
            try:
                return decode_image(image_bytes, media_type)
            except ValueError as exc:
                code = getattr(exc, "code", "invalid_image")
                raise CnnRequestError(code, str(exc), "image") from exc
        raise CnnRequestError(
            "missing_input",
            "Choose a registered sample or upload a PNG/JPEG image.",
            "input",
        )

    @staticmethod
    def _prediction(logits: torch.Tensor) -> dict[str, Any]:
        probabilities = torch.softmax(logits, dim=1)[0].detach().cpu()
        predicted_index = int(torch.argmax(probabilities).item())
        return {
            "predicted_index": predicted_index,
            "predicted_class": CLASS_NAMES[predicted_index],
            "confidence": float(probabilities[predicted_index]),
            "probabilities": [
                {
                    "class_index": index,
                    "class_name": class_name,
                    "probability": float(probabilities[index]),
                }
                for index, class_name in enumerate(CLASS_NAMES)
            ],
        }

    def predict(
        self,
        *,
        sample_id: str | None = None,
        image_bytes: bytes | None = None,
        media_type: str | None = None,
    ) -> dict[str, Any]:
        inputs, input_summary = self._resolve_input(
            sample_id=sample_id,
            image_bytes=image_bytes,
            media_type=media_type,
        )
        with torch.inference_mode():
            logits = self._bundle.model(inputs)
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "model_version": MODEL_VERSION,
            "input": input_summary,
            "prediction": self._prediction(logits),
        }

    def feature_maps(
        self,
        *,
        layer: str,
        channels: tuple[int, ...],
        sample_id: str | None = None,
        image_bytes: bytes | None = None,
        media_type: str | None = None,
    ) -> dict[str, Any]:
        metadata = LAYER_METADATA.get(layer)
        if metadata is None:
            raise CnnRequestError(
                "invalid_layer",
                "The requested layer is not exposed by the published allowlist.",
                "layer",
            )
        if not 1 <= len(channels) <= MAX_CHANNELS_PER_REQUEST:
            raise CnnRequestError(
                "invalid_channel_count",
                f"Select between 1 and {MAX_CHANNELS_PER_REQUEST} channels.",
                "channels",
            )
        if len(set(channels)) != len(channels):
            raise CnnRequestError(
                "duplicate_channel",
                "Channel selections must be unique.",
                "channels",
            )
        channel_count_value = metadata["channels"]
        if not isinstance(channel_count_value, int):
            raise RuntimeError("Published layer metadata contains an invalid channel count.")
        channel_count = channel_count_value
        if any(channel < 0 or channel >= channel_count for channel in channels):
            raise CnnRequestError(
                "invalid_channel",
                f"Channels for {layer} must be between 0 and {channel_count - 1}.",
                "channels",
            )

        inputs, input_summary = self._resolve_input(
            sample_id=sample_id,
            image_bytes=image_bytes,
            media_type=media_type,
        )
        with torch.inference_mode():
            logits, activations = run_with_activations(
                self._bundle.model,
                inputs,
                (layer,),
            )
        activation = activations[layer]
        return {
            "schema_version": SCHEMA_VERSION,
            "module": MODULE_ID,
            "model_version": MODEL_VERSION,
            "input": input_summary,
            "prediction": self._prediction(logits),
            "representation": {
                "layer": {"id": layer, **metadata},
                "activation_tensor_shape": list(activation.shape),
                "maps": [
                    _normalized_map(layer, channel, activation)
                    for channel in channels
                ],
                "comparison_rule": (
                    "Compare spatial patterns only. Each channel uses an independent "
                    "display scale while raw statistics remain available."
                ),
            },
        }
