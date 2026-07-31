from __future__ import annotations

from collections import Counter
from pathlib import Path

import torch
from autoencoder_latent_space.config import DATASET_SOURCE_SHA256
from autoencoder_latent_space.dataset import (
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


def test_autoencoder_split_is_reproducible_and_disjoint() -> None:
    samples = load_official_sprite(_source())
    first = stratified_splits(samples)
    second = stratified_splits(samples)

    assert [sample.source_index for sample in first.train] == [
        sample.source_index for sample in second.train
    ]
    assert (len(first.train), len(first.validation), len(first.test)) == (600, 150, 150)
    identifiers = [
        *(sample.source_index for sample in first.train),
        *(sample.source_index for sample in first.validation),
        *(sample.source_index for sample in first.test),
    ]
    assert len(identifiers) == len(set(identifiers))


def test_autoencoder_augmentation_is_deterministic_and_bounded() -> None:
    training = stratified_splits(load_official_sprite(_source())).train[:2]

    first = tensor_dataset(training, augment=True)
    second = tensor_dataset(training, augment=True)

    assert first.tensors[0].shape == (4, 1, 28, 28)
    assert torch.equal(first.tensors[0], second.tensors[0])
    assert float(first.tensors[0].min()) >= 0.0
    assert float(first.tensors[0].max()) <= 1.0
