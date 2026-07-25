"""Train and register the deterministic Sprint 1 XOR model offline."""

from __future__ import annotations

import json
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

import torch
from torch import nn

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVICE_SOURCE = PROJECT_ROOT / "ai-services" / "neural-network-explainer" / "src"
sys.path.insert(0, str(SERVICE_SOURCE))

from neural_network_explainer.config import (  # noqa: E402
    MODEL_VERSION,
    ModelConfiguration,
    TrainingConfiguration,
)
from neural_network_explainer.dataset import xor_tensors  # noqa: E402
from neural_network_explainer.model import ExplainableXorMlp  # noqa: E402


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    model_configuration = ModelConfiguration()
    training_configuration = TrainingConfiguration()
    torch.manual_seed(training_configuration.seed)
    torch.use_deterministic_algorithms(True)

    features, targets = xor_tensors()
    model = ExplainableXorMlp(model_configuration)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=training_configuration.learning_rate,
    )
    loss_function = nn.BCELoss()
    points: list[dict[str, float | int]] = []

    for epoch in range(training_configuration.epochs + 1):
        predictions = model(features)
        loss = loss_function(predictions, targets)
        if epoch % training_configuration.history_interval == 0:
            points.append({"epoch": epoch, "loss": float(loss.item())})
        if epoch == training_configuration.epochs:
            break
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        probabilities = model(features)
        final_loss = float(loss_function(probabilities, targets).item())
        labels = (probabilities >= training_configuration.threshold).to(torch.float32)
        accuracy = float((labels == targets).to(torch.float32).mean().item())
    if accuracy != 1.0:
        raise RuntimeError("The registered XOR model did not reach the expected accuracy.")

    artifact_directory = PROJECT_ROOT / "models" / "neural-network"
    checkpoint_path = artifact_directory / f"{MODEL_VERSION}.pt"
    artifact_directory.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "model_configuration": model_configuration.to_dict(),
            "training_configuration": training_configuration.to_dict(),
        },
        checkpoint_path,
    )
    checkpoint_bytes = checkpoint_path.read_bytes()
    checkpoint_sha256 = sha256(checkpoint_bytes).hexdigest()
    metrics = {
        "accuracy": accuracy,
        "final_loss": final_loss,
        "predictions": [float(value) for value in probabilities.reshape(-1).tolist()],
    }
    _write_json(
        artifact_directory / "manifest.json",
        {
            "model_version": MODEL_VERSION,
            "framework": f"PyTorch {torch.__version__}",
            "dataset": "xor",
            "checkpoint": checkpoint_path.name,
            "checkpoint_sha256": checkpoint_sha256,
            "checkpoint_bytes": len(checkpoint_bytes),
            "model_configuration": model_configuration.to_dict(),
            "training_configuration": training_configuration.to_dict(),
            "metrics": metrics,
        },
    )
    _write_json(
        artifact_directory / "training-history.json",
        {
            "model_version": MODEL_VERSION,
            "seed": training_configuration.seed,
            "configuration": training_configuration.to_dict(),
            "metrics": {"accuracy": accuracy, "final_loss": final_loss},
            "points": points,
        },
    )
    _write_json(
        PROJECT_ROOT / "reports" / "metrics" / "neural-network" / f"{MODEL_VERSION}.json",
        metrics,
    )
    print(
        f"Registered {MODEL_VERSION}: accuracy={accuracy:.2f}, "
        f"sha256={checkpoint_sha256}"
    )


if __name__ == "__main__":
    main()
