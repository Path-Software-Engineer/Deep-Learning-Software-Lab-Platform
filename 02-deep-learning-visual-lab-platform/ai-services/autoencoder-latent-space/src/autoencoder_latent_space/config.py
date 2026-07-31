"""Versioned contracts for the Fashion-MNIST autoencoder module."""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "1.0"
MODULE_ID = "autoencoder-latent-space-demo"
MODEL_VERSION = "fashion-autoencoder-2d-v1"
DATASET_VERSION = "fashion-mnist-official-sprite-900-v1"
DATASET_SOURCE_SHA256 = (
    "a7de0a151f8c68e6e96f157a018ac290d1f6b0e7845892c3d7d85cb64961c3cb"
)
CLASS_NAMES = (
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
)
REFERENCE_POINTS_PER_CLASS = 10
NEIGHBOR_COUNT = 5
MIN_INTERPOLATION_STEPS = 3
MAX_INTERPOLATION_STEPS = 12

LIMITATIONS = (
    "The two-dimensional bottleneck sacrifices reconstruction capacity to make "
    "the representation directly visible.",
    "Latent proximity is Euclidean distance inside this registered model and "
    "does not guarantee universal semantic similarity.",
    "A smooth interpolation shows decoder continuity along one segment; it "
    "does not demonstrate understanding or causality.",
    "Fashion-MNIST is an educational benchmark and this release uses a curated "
    "900-image official sprite rather than the complete dataset.",
    "The registered model and held-out reconstruction metrics are controlled "
    "portfolio evidence, not production-readiness evidence.",
)


@dataclass(frozen=True, slots=True)
class ModelConfiguration:
    input_channels: int = 1
    image_size: int = 28
    encoder_channels_one: int = 16
    encoder_channels_two: int = 32
    hidden_features: int = 64
    latent_dimensions: int = 2


@dataclass(frozen=True, slots=True)
class PreprocessingConfiguration:
    color_mode: str = "grayscale"
    image_size: tuple[int, int] = (28, 28)
    value_range: tuple[float, float] = (0.0, 1.0)
    normalization: str = "pixel-divided-by-255"
    reconstruction_output: str = "sigmoid-bounded-0-to-1"


@dataclass(frozen=True, slots=True)
class TrainingConfiguration:
    seed: int = 20_260_729
    epochs: int = 90
    batch_size: int = 64
    learning_rate: float = 0.001
    weight_decay: float = 0.00001
    optimizer: str = "Adam"
    loss_function: str = "MSELoss"
    train_per_class: int = 60
    validation_per_class: int = 15
    test_per_class: int = 15
    augmentation_copies: int = 1


MODEL_CONFIGURATION = ModelConfiguration()
PREPROCESSING_CONFIGURATION = PreprocessingConfiguration()
TRAINING_CONFIGURATION = TrainingConfiguration()
