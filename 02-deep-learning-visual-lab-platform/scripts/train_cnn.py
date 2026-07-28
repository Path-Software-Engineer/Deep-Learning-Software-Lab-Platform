"""Train, evaluate and register the Sprint 2 Fashion-MNIST CNN."""

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
CNN_SOURCE = PROJECT_ROOT / "ai-services" / "cnn-feature-map-viewer" / "src"
sys.path.insert(0, str(CNN_SOURCE))

from cnn_feature_map_viewer.config import (  # noqa: E402
    CLASS_NAMES,
    DATASET_VERSION,
    MODEL_CONFIGURATION,
    MODEL_VERSION,
    PREPROCESSING_CONFIGURATION,
    TRAINING_CONFIGURATION,
)
from cnn_feature_map_viewer.dataset import (  # noqa: E402
    FashionSample,
    load_official_sprite,
    sha256_file,
    stratified_splits,
    tensor_dataset,
)
from cnn_feature_map_viewer.model import FashionCnn  # noqa: E402


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
    model: FashionCnn,
    dataset: TensorDataset,
    loss_function: nn.Module,
) -> dict[str, Any]:
    loader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=0)
    losses: list[float] = []
    predictions: list[torch.Tensor] = []
    targets: list[torch.Tensor] = []
    model.eval()
    with torch.inference_mode():
        for features, labels in loader:
            logits = model(features)
            losses.append(float(loss_function(logits, labels).item()) * len(labels))
            predictions.append(torch.argmax(logits, dim=1))
            targets.append(labels)
    predicted = torch.cat(predictions)
    target = torch.cat(targets)
    confusion = torch.zeros((len(CLASS_NAMES), len(CLASS_NAMES)), dtype=torch.int64)
    for expected, observed in zip(target.tolist(), predicted.tolist(), strict=True):
        confusion[expected, observed] += 1
    per_class = []
    for index, class_name in enumerate(CLASS_NAMES):
        total = int(confusion[index].sum())
        correct = int(confusion[index, index])
        per_class.append(
            {
                "class_index": index,
                "class_name": class_name,
                "correct": correct,
                "total": total,
                "accuracy": correct / total if total else 0.0,
            }
        )
    return {
        "samples": int(len(target)),
        "loss": sum(losses) / len(target),
        "accuracy": float((predicted == target).float().mean().item()),
        "correct": int((predicted == target).sum().item()),
        "confusion_matrix": confusion.tolist(),
        "per_class": per_class,
    }


def _sample_gallery(
    model: FashionCnn,
    samples: tuple[FashionSample, ...],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    model.eval()
    for label_index, class_name in enumerate(CLASS_NAMES):
        candidates = [sample for sample in samples if sample.label_index == label_index]
        dataset = tensor_dataset(tuple(candidates))
        features = dataset.tensors[0]
        with torch.inference_mode():
            probabilities = torch.softmax(model(features), dim=1)
        predictions = torch.argmax(probabilities, dim=1)
        correct = [
            index
            for index, prediction in enumerate(predictions.tolist())
            if prediction == label_index
        ]
        eligible = correct or list(range(len(candidates)))
        selected_index = max(
            eligible,
            key=lambda index: float(probabilities[index, label_index]),
        )
        sample = candidates[selected_index]
        result.append(
            {
                "id": f"fashion-{label_index:02d}",
                "source_index": sample.source_index,
                "label_index": label_index,
                "label": class_name,
                "registered_prediction": CLASS_NAMES[int(predictions[selected_index])],
                "registered_confidence": float(probabilities[selected_index].max()),
                "pixels": (
                    torch.clamp(sample.pixels.squeeze(0), 0.0, 1.0)
                    .mul(255)
                    .round()
                    .to(torch.uint8)
                    .tolist()
                ),
            }
        )
    return result


def _write_summary(
    path: Path,
    *,
    evaluation: dict[str, Any],
    source_sha256: str,
    checkpoint_sha256: str,
    elapsed_seconds: float,
) -> None:
    lines = [
        "# CNN Feature Map Viewer — registered model evidence",
        "",
        "## Dataset",
        "",
        "- Source: Zalando Research official Fashion-MNIST sprite.",
        f"- Source SHA-256: `{source_sha256}`.",
        "- Controlled subset: 900 images, 90 per class.",
        "- Split: 600 training, 150 validation, 150 held-out evaluation images.",
        "",
        "## Model",
        "",
        f"- Version: `{MODEL_VERSION}`.",
        "- Architecture: two Conv-BatchNorm-ReLU-Pool blocks and a 128-unit classifier.",
        f"- Checkpoint SHA-256: `{checkpoint_sha256}`.",
        f"- Training duration on the recorded CPU run: {elapsed_seconds:.2f} seconds.",
        "",
        "## Held-out evidence",
        "",
        (
            f"- Accuracy: {evaluation['accuracy']:.4f} "
            f"({evaluation['correct']}/{evaluation['samples']})."
        ),
        f"- Cross-entropy loss: {evaluation['loss']:.6f}.",
        "",
        "## Evidence boundary",
        "",
        "This registered model is an educational release built from a curated official sprite,",
        "not the complete Fashion-MNIST benchmark. Feature maps are intermediate activations,",
        "not causal explanations, saliency maps or production-readiness evidence.",
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

    generator = torch.Generator().manual_seed(configuration.seed)
    loader = DataLoader(
        training_dataset,
        batch_size=configuration.batch_size,
        shuffle=True,
        generator=generator,
        num_workers=0,
    )
    model = FashionCnn(MODEL_CONFIGURATION)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=configuration.learning_rate,
        weight_decay=configuration.weight_decay,
    )
    loss_function = nn.CrossEntropyLoss()
    history: list[dict[str, float | int]] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_accuracy = -1.0
    best_loss = float("inf")
    started = time.perf_counter()

    for epoch in range(1, configuration.epochs + 1):
        model.train()
        total_loss = 0.0
        seen = 0
        for features, labels in loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(features)
            loss = loss_function(logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item()) * len(labels)
            seen += len(labels)
        validation = _evaluate(model, validation_dataset, loss_function)
        training_loss = total_loss / seen
        history.append(
            {
                "epoch": epoch,
                "training_loss": training_loss,
                "validation_loss": float(validation["loss"]),
                "validation_accuracy": float(validation["accuracy"]),
            }
        )
        accuracy = float(validation["accuracy"])
        validation_loss = float(validation["loss"])
        if accuracy > best_accuracy or (
            accuracy == best_accuracy and validation_loss < best_loss
        ):
            best_accuracy = accuracy
            best_loss = validation_loss
            best_state = {
                name: tensor.detach().cpu().clone()
                for name, tensor in model.state_dict().items()
            }

    if best_state is None:
        raise RuntimeError("Training did not produce a candidate checkpoint.")
    model.load_state_dict(best_state, strict=True)
    model.eval()
    elapsed_seconds = time.perf_counter() - started
    evaluation = _evaluate(model, test_dataset, loss_function)
    validation = _evaluate(model, validation_dataset, loss_function)

    destination = PROJECT_ROOT / "models" / "cnn"
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

    sample_gallery = {
        "model_version": MODEL_VERSION,
        "dataset_version": DATASET_VERSION,
        "samples": _sample_gallery(model, splits.test),
    }
    gallery_path = destination / "sample-gallery.json"
    _write_json(gallery_path, sample_gallery)
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
        "sample_gallery": gallery_path.name,
        "sample_gallery_sha256": _sha256(gallery_path),
        "model_configuration": model_data,
        "training_configuration": training_data,
        "preprocessing_configuration": preprocessing_data,
        "classes": list(CLASS_NAMES),
        "validation": validation,
        "evaluation": evaluation,
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

    metrics_destination = PROJECT_ROOT / "reports" / "metrics" / "cnn"
    _write_json(
        metrics_destination / f"{MODEL_VERSION}.json",
        {
            "model_version": MODEL_VERSION,
            "validation": validation,
            "evaluation": evaluation,
            "training_seconds": elapsed_seconds,
        },
    )
    _write_summary(
        PROJECT_ROOT / "reports" / "summaries" / "cnn" / f"{MODEL_VERSION}.md",
        evaluation=evaluation,
        source_sha256=source_sha256,
        checkpoint_sha256=checkpoint_sha256,
        elapsed_seconds=elapsed_seconds,
    )

    print(f"Registered CNN checkpoint: {checkpoint}")
    print(f"Validation accuracy: {float(validation['accuracy']):.4f}")
    print(
        "Held-out accuracy: "
        f"{float(evaluation['accuracy']):.4f} "
        f"({evaluation['correct']}/{evaluation['samples']})"
    )
    print(f"Held-out loss: {float(evaluation['loss']):.6f}")
    print(f"Training seconds: {elapsed_seconds:.2f}")


if __name__ == "__main__":
    main()
