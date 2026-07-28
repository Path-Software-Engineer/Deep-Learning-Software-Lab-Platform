from __future__ import annotations

from collections import Counter
from pathlib import Path

import torch
from cnn_feature_map_viewer.config import DATASET_SOURCE_SHA256
from cnn_feature_map_viewer.dataset import (
    load_official_sprite,
    sha256_file,
    stratified_splits,
    tensor_dataset,
)


def _source() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "data"
        / "raw"
        / "fashion-mnist-official"
        / "fashion-mnist-sprite.png"
    )


def test_official_sprite_contract_is_integrity_checked() -> None:
    source = _source()
    samples = load_official_sprite(source)

    assert sha256_file(source) == DATASET_SOURCE_SHA256
    assert len(samples) == 900
    assert samples[0].pixels.shape == (1, 28, 28)
    assert Counter(sample.label_index for sample in samples) == Counter(
        {index: 90 for index in range(10)}
    )


def test_stratified_split_is_reproducible_and_disjoint() -> None:
    samples = load_official_sprite(_source())
    first = stratified_splits(samples)
    second = stratified_splits(samples)

    assert [sample.source_index for sample in first.train] == [
        sample.source_index for sample in second.train
    ]
    assert len(first.train) == 600
    assert len(first.validation) == 150
    assert len(first.test) == 150
    identifiers = [
        *(sample.source_index for sample in first.train),
        *(sample.source_index for sample in first.validation),
        *(sample.source_index for sample in first.test),
    ]
    assert len(identifiers) == len(set(identifiers))


def test_training_tensor_dataset_adds_deterministic_augmentation() -> None:
    samples = load_official_sprite(_source())
    training = stratified_splits(samples).train[:2]

    first = tensor_dataset(training, augment=True)
    second = tensor_dataset(training, augment=True)

    assert first.tensors[0].shape == (6, 1, 28, 28)
    assert torch.equal(first.tensors[0], second.tensors[0])
    assert torch.equal(first.tensors[1], second.tensors[1])
