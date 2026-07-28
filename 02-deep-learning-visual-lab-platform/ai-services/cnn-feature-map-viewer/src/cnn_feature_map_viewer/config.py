"""Versioned contracts for the Fashion-MNIST CNN feature-map module."""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "1.0"
MODULE_ID = "cnn-feature-map-viewer"
MODEL_VERSION = "fashion-cnn-v1"
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
MAX_CHANNELS_PER_REQUEST = 12
MAX_IMAGE_BYTES = 1_048_576
MAX_IMAGE_DIMENSION = 1_024
ALLOWED_MEDIA_TYPES = ("image/png", "image/jpeg")

LIMITATIONS = (
    "Feature maps expose intermediate activations, not causal explanations.",
    "Each channel is normalized independently for display, so color intensity "
    "is not comparable across maps.",
    "The registered model uses a curated 900-image official Fashion-MNIST "
    "sprite, not the complete 70,000-image benchmark.",
    "The held-out evaluation contains 150 images and is evidence for this controlled release only.",
    "Prediction confidence is model output context, not proof that a visible "
    "region caused the decision.",
)


@dataclass(frozen=True, slots=True)
class ModelConfiguration:
    input_channels: int = 1
    image_size: int = 28
    conv1_channels: int = 16
    conv2_channels: int = 32
    hidden_features: int = 128
    dropout: float = 0.25
    class_count: int = len(CLASS_NAMES)


@dataclass(frozen=True, slots=True)
class PreprocessingConfiguration:
    color_mode: str = "grayscale"
    image_size: tuple[int, int] = (28, 28)
    value_range: tuple[float, float] = (0.0, 1.0)
    resize_policy: str = "bilinear-to-28x28"
    normalization: str = "(pixel-mean)/std"
    mean: float = 0.2860406
    std: float = 0.35302424


@dataclass(frozen=True, slots=True)
class TrainingConfiguration:
    seed: int = 20_260_728
    epochs: int = 30
    batch_size: int = 64
    learning_rate: float = 0.001
    weight_decay: float = 0.0001
    optimizer: str = "Adam"
    loss_function: str = "CrossEntropyLoss"
    train_per_class: int = 60
    validation_per_class: int = 15
    test_per_class: int = 15
    augmentation_copies: int = 2


MODEL_CONFIGURATION = ModelConfiguration()
PREPROCESSING_CONFIGURATION = PreprocessingConfiguration()
TRAINING_CONFIGURATION = TrainingConfiguration()

LAYER_METADATA = {
    "block1_relu": {
        "label": "Edge and contour bank",
        "operation": "Conv2d 3x3 + BatchNorm2d + ReLU",
        "channels": MODEL_CONFIGURATION.conv1_channels,
        "tensor_shape": [1, MODEL_CONFIGURATION.conv1_channels, 28, 28],
    },
    "block2_relu": {
        "label": "Composed texture bank",
        "operation": "Conv2d 3x3 + BatchNorm2d + ReLU after 2x2 max pooling",
        "channels": MODEL_CONFIGURATION.conv2_channels,
        "tensor_shape": [1, MODEL_CONFIGURATION.conv2_channels, 14, 14],
    },
}
