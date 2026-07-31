"""Train, evaluate and register the Sprint 3 two-dimensional autoencoder."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUTOENCODER_SOURCE = (
    PROJECT_ROOT / "ai-services" / "autoencoder-latent-space" / "src"
)
sys.path.insert(0, str(AUTOENCODER_SOURCE))

from autoencoder_latent_space.config import (  # noqa: E402
    CLASS_NAMES,
    DATASET_VERSION,
    MODEL_CONFIGURATION,
    MODEL_VERSION,
    PREPROCESSING_CONFIGURATION,
    REFERENCE_POINTS_PER_CLASS,
    TRAINING_CONFIGURATION,
)
from autoencoder_latent_space.dataset import (  # noqa: E402
    FashionSample,
    load_official_sprite,
    sha256_file,
    stratified_splits,
    tensor_dataset,
)
from autoencoder_latent_space.model import FashionAutoencoder  # noqa: E402


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _evaluate(
    model: FashionAutoencoder,
    dataset: TensorDataset,
) -> dict[str, float | int]:
    loader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=0)
    squared_error = 0.0
    absolute_error = 0.0
    pixel_count = 0
    model.eval()
    with torch.inference_mode():
        for images, _ in loader:
            reconstructed, _ = model(images)
            squared_error += float(torch.sum((reconstructed - images) ** 2).item())
            absolute_error += float(torch.sum(torch.abs(reconstructed - images)).item())
            pixel_count += images.numel()
    return {
        "samples": len(dataset),
        "mean_squared_error": squared_error / pixel_count,
        "mean_absolute_error": absolute_error / pixel_count,
        "pixels_evaluated": pixel_count,
    }


def _latent_gallery(
    model: FashionAutoencoder,
    samples: tuple[FashionSample, ...],
) -> tuple[list[dict[str, Any]], dict[str, list[float]]]:
    selected: list[FashionSample] = []
    for label_index in range(len(CLASS_NAMES)):
        candidates = [
            sample for sample in samples if sample.label_index == label_index
        ]
        selected.extend(candidates[:REFERENCE_POINTS_PER_CLASS])
    dataset = tensor_dataset(tuple(selected))
    images = dataset.tensors[0]
    model.eval()
    with torch.inference_mode():
        reconstructed, coordinates = model(images)
    point_errors = torch.mean((reconstructed - images) ** 2, dim=(1, 2, 3))
    points: list[dict[str, Any]] = []
    class_positions = {index: 0 for index in range(len(CLASS_NAMES))}
    for index, sample in enumerate(selected):
        position = class_positions[sample.label_index]
        class_positions[sample.label_index] += 1
        points.append(
            {
                "id": f"latent-{sample.label_index:02d}-{position:02d}",
                "source_index": sample.source_index,
                "label_index": sample.label_index,
                "label": CLASS_NAMES[sample.label_index],
                "coordinate": [
                    round(float(value), 6)
                    for value in coordinates[index].tolist()
                ],
                "reconstruction_error": float(point_errors[index]),
                "pixels": (
                    sample.pixels.squeeze(0)
                    .mul(255)
                    .round()
                    .to(torch.uint8)
                    .tolist()
                ),
            }
        )
    minimum = coordinates.min(dim=0).values
    maximum = coordinates.max(dim=0).values
    span = torch.clamp(maximum - minimum, min=1.0)
    padding = span * 0.08
    bounds = {
        "x": [float(minimum[0] - padding[0]), float(maximum[0] + padding[0])],
        "y": [float(minimum[1] - padding[1]), float(maximum[1] + padding[1])],
    }
    return points, bounds


def _write_summary(
    path: Path,
    *,
    evaluation: dict[str, float | int],
    validation: dict[str, float | int],
    checkpoint_sha256: str,
    source_sha256: str,
    elapsed_seconds: float,
) -> None:
    lines = [
        "# Autoencoder Latent Space Demo — registered model evidence",
        "",
        "## Dataset",
        "",
        "- Source: Zalando Research official Fashion-MNIST sprite.",
        f"- Source SHA-256: `{source_sha256}`.",
        "- Controlled subset: 900 images, 90 per class.",
        "- Split: 600 training, 150 validation and 150 held-out test images.",
        "",
        "## Model",
        "",
        f"- Version: `{MODEL_VERSION}`.",
        "- Architecture: convolutional encoder, 2D bottleneck and convolutional decoder.",
        f"- Checkpoint SHA-256: `{checkpoint_sha256}`.",
        f"- Recorded CPU training duration: {elapsed_seconds:.2f} seconds.",
        "",
        "## Reconstruction evidence",
        "",
        f"- Validation MSE: {float(validation['mean_squared_error']):.6f}.",
        f"- Validation MAE: {float(validation['mean_absolute_error']):.6f}.",
        f"- Held-out MSE: {float(evaluation['mean_squared_error']):.6f}.",
        f"- Held-out MAE: {float(evaluation['mean_absolute_error']):.6f}.",
        "",
        "## Evidence boundary",
        "",
        "The two-dimensional bottleneck is intentionally restrictive and makes the",
        "representation visible at the cost of reconstruction capacity. Distance and",
        "interpolation belong only to this registered model; neither is a causal or",
        "universal semantic explanation.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    configuration = TRAINING_CONFIGURATION
    torch.manual_seed(configuration.seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)

    source = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "fashion-mnist-official"
        / "fashion-mnist-sprite.png"
    )
    samples = load_official_sprite(source)
    splits = stratified_splits(samples)
    training_dataset = tensor_dataset(splits.train, augment=True)
    validation_dataset = tensor_dataset(splits.validation)
    test_dataset = tensor_dataset(splits.test)
    loader = DataLoader(
        training_dataset,
        batch_size=configuration.batch_size,
        shuffle=True,
        generator=torch.Generator().manual_seed(configuration.seed),
        num_workers=0,
    )
    model = FashionAutoencoder(MODEL_CONFIGURATION)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=configuration.learning_rate,
        weight_decay=configuration.weight_decay,
    )
    loss_function = nn.MSELoss()
    history: list[dict[str, float | int]] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_validation_loss = float("inf")
    started = time.perf_counter()

    for epoch in range(1, configuration.epochs + 1):
        model.train()
        total_loss = 0.0
        seen = 0
        for images, _ in loader:
            optimizer.zero_grad(set_to_none=True)
            reconstructed, _ = model(images)
            loss = loss_function(reconstructed, images)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item()) * len(images)
            seen += len(images)
        validation = _evaluate(model, validation_dataset)
        validation_loss = float(validation["mean_squared_error"])
        history.append(
            {
                "epoch": epoch,
                "training_loss": total_loss / seen,
                "validation_loss": validation_loss,
            }
        )
        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            best_state = {
                name: tensor.detach().cpu().clone()
                for name, tensor in model.state_dict().items()
            }

    if best_state is None:
        raise RuntimeError("Training did not produce an autoencoder checkpoint.")
    model.load_state_dict(best_state, strict=True)
    model.eval()
    elapsed_seconds = time.perf_counter() - started
    validation = _evaluate(model, validation_dataset)
    evaluation = _evaluate(model, test_dataset)
    gallery, bounds = _latent_gallery(model, splits.test)

    destination = PROJECT_ROOT / "models" / "autoencoder"
    destination.mkdir(parents=True, exist_ok=True)
    checkpoint = destination / f"{MODEL_VERSION}.pt"
    model_data = asdict(MODEL_CONFIGURATION)
    training_data = asdict(TRAINING_CONFIGURATION)
    preprocessing_data = asdict(PREPROCESSING_CONFIGURATION)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "model_configuration": model_data,
            "training_configuration": training_data,
            "preprocessing_configuration": preprocessing_data,
            "dataset_version": DATASET_VERSION,
        },
        checkpoint,
    )
    gallery_path = destination / "latent-gallery.json"
    _write_json(
        gallery_path,
        {
            "model_version": MODEL_VERSION,
            "dataset_version": DATASET_VERSION,
            "points": gallery,
        },
    )
    source_sha256 = sha256_file(source)
    checkpoint_sha256 = _sha256(checkpoint)
    manifest = {
        "model_version": MODEL_VERSION,
        "framework": f"PyTorch {torch.__version__}",
        "dataset_version": DATASET_VERSION,
        "dataset_source": (
            "https://github.com/zalandoresearch/fashion-mnist/"
            "blob/master/doc/img/fashion-mnist-sprite.png"
        ),
        "dataset_source_sha256": source_sha256,
        "checkpoint": checkpoint.name,
        "checkpoint_sha256": checkpoint_sha256,
        "checkpoint_bytes": checkpoint.stat().st_size,
        "latent_gallery": gallery_path.name,
        "latent_gallery_sha256": _sha256(gallery_path),
        "model_configuration": model_data,
        "training_configuration": training_data,
        "preprocessing_configuration": preprocessing_data,
        "validation": validation,
        "evaluation": evaluation,
        "latent_bounds": bounds,
        "training_seconds": elapsed_seconds,
    }
    training_history = {
        "model_version": MODEL_VERSION,
        "dataset_version": DATASET_VERSION,
        "configuration": training_data,
        "selected_validation": validation,
        "evaluation": evaluation,
        "points": history,
    }
    _write_json(destination / "manifest.json", manifest)
    _write_json(destination / "training-history.json", training_history)
    _write_json(
        PROJECT_ROOT
        / "reports"
        / "metrics"
        / "autoencoder"
        / f"{MODEL_VERSION}.json",
        {
            "model_version": MODEL_VERSION,
            "validation": validation,
            "evaluation": evaluation,
            "training_seconds": elapsed_seconds,
            "reference_points": len(gallery),
            "latent_bounds": bounds,
        },
    )
    _write_summary(
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "autoencoder"
        / f"{MODEL_VERSION}.md",
        evaluation=evaluation,
        validation=validation,
        checkpoint_sha256=checkpoint_sha256,
        source_sha256=source_sha256,
        elapsed_seconds=elapsed_seconds,
    )
    print(f"Registered autoencoder checkpoint: {checkpoint}")
    print(f"Validation MSE: {float(validation['mean_squared_error']):.6f}")
    print(f"Held-out MSE: {float(evaluation['mean_squared_error']):.6f}")
    print(f"Held-out MAE: {float(evaluation['mean_absolute_error']):.6f}")
    print(f"Latent reference points: {len(gallery)}")
    print(f"Training seconds: {elapsed_seconds:.2f}")


if __name__ == "__main__":
    main()
