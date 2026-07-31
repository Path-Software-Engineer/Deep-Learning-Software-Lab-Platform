"""Deterministic Fashion-MNIST sprite extraction for autoencoder training."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import torch
from PIL import Image
from torch.utils.data import TensorDataset

from autoencoder_latent_space.config import (
    CLASS_NAMES,
    DATASET_SOURCE_SHA256,
    TRAINING_CONFIGURATION,
)

SPRITE_COLUMNS = 30
SPRITE_ROWS = 30
SAMPLES_PER_CLASS = 90


@dataclass(frozen=True, slots=True)
class FashionSample:
    source_index: int
    label_index: int
    pixels: torch.Tensor


@dataclass(frozen=True, slots=True)
class DatasetSplits:
    train: tuple[FashionSample, ...]
    validation: tuple[FashionSample, ...]
    test: tuple[FashionSample, ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_official_sprite(path: Path) -> tuple[FashionSample, ...]:
    if not path.is_file():
        raise FileNotFoundError(
            "The official Fashion-MNIST sprite is missing. See docs/data-contract.md."
        )
    if sha256_file(path) != DATASET_SOURCE_SHA256:
        raise ValueError("The official Fashion-MNIST sprite checksum does not match.")
    with Image.open(path) as image:
        grayscale = image.convert("L")
        if grayscale.size != (840, 840):
            raise ValueError("The Fashion-MNIST sprite must be 840x840 pixels.")
        values = torch.tensor(list(grayscale.getdata()), dtype=torch.float32)
        grid = values.reshape(840, 840) / 255.0
    samples: list[FashionSample] = []
    for index in range(SPRITE_COLUMNS * SPRITE_ROWS):
        row, column = divmod(index, SPRITE_COLUMNS)
        samples.append(
            FashionSample(
                source_index=index,
                label_index=index // SAMPLES_PER_CLASS,
                pixels=grid[
                    row * 28 : (row + 1) * 28,
                    column * 28 : (column + 1) * 28,
                ]
                .unsqueeze(0)
                .clone(),
            )
        )
    return tuple(samples)


def stratified_splits(
    samples: tuple[FashionSample, ...],
    *,
    seed: int = TRAINING_CONFIGURATION.seed,
) -> DatasetSplits:
    expected = len(CLASS_NAMES) * SAMPLES_PER_CLASS
    if len(samples) != expected:
        raise ValueError(f"Expected {expected} Fashion-MNIST sprite samples.")
    generator = torch.Generator().manual_seed(seed)
    train: list[FashionSample] = []
    validation: list[FashionSample] = []
    test: list[FashionSample] = []
    for label_index in range(len(CLASS_NAMES)):
        candidates = [
            sample for sample in samples if sample.label_index == label_index
        ]
        order = torch.randperm(len(candidates), generator=generator).tolist()
        ordered = [candidates[index] for index in order]
        train_end = TRAINING_CONFIGURATION.train_per_class
        validation_end = train_end + TRAINING_CONFIGURATION.validation_per_class
        test_end = validation_end + TRAINING_CONFIGURATION.test_per_class
        train.extend(ordered[:train_end])
        validation.extend(ordered[train_end:validation_end])
        test.extend(ordered[validation_end:test_end])
    return DatasetSplits(tuple(train), tuple(validation), tuple(test))


def _augmented_copy(
    pixels: torch.Tensor,
    *,
    generator: torch.Generator,
) -> torch.Tensor:
    shift_x = int(torch.randint(-1, 2, (1,), generator=generator).item())
    shift_y = int(torch.randint(-1, 2, (1,), generator=generator).item())
    transformed = torch.roll(pixels, shifts=(shift_y, shift_x), dims=(1, 2))
    if shift_y > 0:
        transformed[:, :shift_y, :] = 0
    elif shift_y < 0:
        transformed[:, shift_y:, :] = 0
    if shift_x > 0:
        transformed[:, :, :shift_x] = 0
    elif shift_x < 0:
        transformed[:, :, shift_x:] = 0
    return transformed


def tensor_dataset(
    samples: tuple[FashionSample, ...],
    *,
    augment: bool = False,
    seed: int = TRAINING_CONFIGURATION.seed,
) -> TensorDataset:
    generator = torch.Generator().manual_seed(seed)
    images: list[torch.Tensor] = []
    labels: list[int] = []
    for sample in samples:
        images.append(sample.pixels)
        labels.append(sample.label_index)
        if augment:
            for _ in range(TRAINING_CONFIGURATION.augmentation_copies):
                images.append(_augmented_copy(sample.pixels, generator=generator))
                labels.append(sample.label_index)
    return TensorDataset(
        torch.stack(images),
        torch.tensor(labels, dtype=torch.long),
    )


def dataset_metadata() -> dict[str, object]:
    configuration = TRAINING_CONFIGURATION
    return {
        "name": "Fashion-MNIST",
        "version": "official-sprite-900-v1",
        "source": "Zalando Research official Fashion-MNIST repository sprite",
        "source_sha256": DATASET_SOURCE_SHA256,
        "classes": list(CLASS_NAMES),
        "available_samples": 900,
        "image_shape": [1, 28, 28],
        "split": {
            "training": configuration.train_per_class * len(CLASS_NAMES),
            "validation": configuration.validation_per_class * len(CLASS_NAMES),
            "test": configuration.test_per_class * len(CLASS_NAMES),
            "stratified": True,
        },
    }
