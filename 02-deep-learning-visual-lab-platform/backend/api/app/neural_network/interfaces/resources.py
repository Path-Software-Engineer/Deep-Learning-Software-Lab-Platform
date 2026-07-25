"""Pydantic resources defining the public Sprint 1 contract."""

from __future__ import annotations

from pydantic import Field, field_validator

from app.common.resources import StrictResource


class DatasetResource(StrictResource):
    name: str
    description: str
    samples: int = Field(gt=0)
    features: int = Field(gt=0)
    targets: int = Field(gt=0)
    points: list[list[float]] = Field(min_length=4, max_length=4)
    labels: list[int] = Field(min_length=4, max_length=4)


class ArchitectureResource(StrictResource):
    input_nodes: int = Field(gt=0)
    hidden_nodes: int = Field(gt=0)
    output_nodes: int = Field(gt=0)
    hidden_activation: str
    output_activation: str
    parameter_count: int = Field(gt=0)


class CheckpointResource(StrictResource):
    file: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    bytes: int = Field(gt=0)


class NeuralNetworkSummaryResource(StrictResource):
    module_id: str
    name: str
    status: str
    model_version: str
    dataset: DatasetResource
    architecture: ArchitectureResource
    checkpoint: CheckpointResource
    engine: str
    limitations: list[str] = Field(min_length=1)


class ForwardRequest(StrictResource):
    inputs: tuple[float, float]

    @field_validator("inputs")
    @classmethod
    def validate_binary_inputs(
        cls,
        values: tuple[float, float],
    ) -> tuple[float, float]:
        if any(value not in (0.0, 1.0) for value in values):
            raise ValueError("each XOR input must be 0 or 1")
        return values


class LayerResource(StrictResource):
    id: str
    label: str
    operation: str
    weights: list[list[float]]
    biases: list[float]
    preactivations: list[float]
    activations: list[float]


class ForwardResource(StrictResource):
    inputs: list[float] = Field(min_length=2, max_length=2)
    layers: list[LayerResource] = Field(min_length=2, max_length=2)
    output: float = Field(ge=0.0, le=1.0)
    target: int = Field(ge=0, le=1)
    loss: float = Field(ge=0.0)
    prediction: int = Field(ge=0, le=1)
    threshold: float = Field(gt=0.0, lt=1.0)
    model_version: str
    checkpoint_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    limitations: list[str] = Field(min_length=1)

    @field_validator("layers")
    @classmethod
    def validate_layer_order(cls, layers: list[LayerResource]) -> list[LayerResource]:
        if [layer.id for layer in layers] != ["hidden", "output"]:
            raise ValueError("the registered layer order must be hidden, then output")
        return layers


class TrainingPointResource(StrictResource):
    epoch: int = Field(ge=0)
    loss: float = Field(ge=0.0)


class TrainingConfigurationResource(StrictResource):
    seed: int
    epochs: int = Field(gt=0)
    learning_rate: float = Field(gt=0.0)
    optimizer: str
    loss_function: str
    history_interval: int = Field(gt=0)
    threshold: float = Field(gt=0.0, lt=1.0)


class TrainingMetricsResource(StrictResource):
    accuracy: float = Field(ge=0.0, le=1.0)
    final_loss: float = Field(ge=0.0)


class TrainingHistoryResource(StrictResource):
    model_version: str
    seed: int
    configuration: TrainingConfigurationResource
    metrics: TrainingMetricsResource
    points: list[TrainingPointResource] = Field(min_length=1)
    limitations: list[str] = Field(min_length=1)
