"""Artifact-backed application service for real PyTorch forward traces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
from torch.nn.functional import binary_cross_entropy

from neural_network_explainer.artifacts import ArtifactBundle, load_artifact_bundle
from neural_network_explainer.config import LIMITATIONS, MODEL_VERSION
from neural_network_explainer.dataset import XOR_LABELS, XOR_POINTS, validate_xor_inputs, xor_target
from neural_network_explainer.snapshot import build_layer_snapshot


class NeuralNetworkExplainer:
    def __init__(self, artifact_directory: Path) -> None:
        self._bundle: ArtifactBundle = load_artifact_bundle(artifact_directory)

    def summary(self) -> dict[str, Any]:
        model = self._bundle.model
        return {
            "module_id": "neural-network-explainer",
            "name": "Neural Network Explainer",
            "status": "available",
            "model_version": MODEL_VERSION,
            "dataset": {
                "name": "xor",
                "description": "Controlled binary XOR truth table.",
                "samples": len(XOR_POINTS),
                "features": 2,
                "targets": 1,
                "points": [list(point) for point in XOR_POINTS],
                "labels": list(XOR_LABELS),
            },
            "architecture": {
                "input_nodes": model.configuration.input_size,
                "hidden_nodes": model.configuration.hidden_size,
                "output_nodes": model.configuration.output_size,
                "hidden_activation": model.configuration.hidden_activation,
                "output_activation": model.configuration.output_activation,
                "parameter_count": model.parameter_count,
            },
            "checkpoint": {
                "file": f"{MODEL_VERSION}.pt",
                "sha256": self._bundle.checkpoint_sha256,
                "bytes": self._bundle.checkpoint_bytes,
            },
            "engine": "PyTorch",
            "limitations": list(LIMITATIONS),
        }

    def forward(self, inputs: tuple[float, float]) -> dict[str, Any]:
        validated = validate_xor_inputs(inputs)
        features = torch.tensor([validated], dtype=torch.float32)
        target = xor_target(validated)
        target_tensor = torch.tensor([[float(target)]], dtype=torch.float32)
        with torch.no_grad():
            output, state = self._bundle.model.forward_with_state(features)
            loss = binary_cross_entropy(output, target_tensor)

        probability = float(output.item())
        threshold = float(self._bundle.history["configuration"]["threshold"])
        return {
            "inputs": list(validated),
            "layers": build_layer_snapshot(self._bundle.model, state),
            "output": probability,
            "target": target,
            "loss": float(loss.item()),
            "prediction": int(probability >= threshold),
            "threshold": threshold,
            "model_version": MODEL_VERSION,
            "checkpoint_sha256": self._bundle.checkpoint_sha256,
            "limitations": list(LIMITATIONS),
        }

    def training_history(self) -> dict[str, Any]:
        history = dict(self._bundle.history)
        history["limitations"] = list(LIMITATIONS)
        return history
