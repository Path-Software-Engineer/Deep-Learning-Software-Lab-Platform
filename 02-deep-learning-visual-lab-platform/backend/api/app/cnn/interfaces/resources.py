"""Pydantic resources for the public Sprint 2 CNN contract."""

from __future__ import annotations

from pydantic import Field

from app.common.resources import StrictResource


class CnnCheckpointResource(StrictResource):
    file: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    bytes: int = Field(gt=0)


class CnnModelResource(StrictResource):
    name: str
    version: str
    framework: str
    architecture: str
    parameter_count: int = Field(gt=0)
    input_shape: list[int] = Field(min_length=3, max_length=3)
    output_shape: list[int] = Field(min_length=1, max_length=1)
    dataset: str
    checkpoint: CnnCheckpointResource


class CnnDatasetSplitResource(StrictResource):
    training: int = Field(gt=0)
    validation: int = Field(gt=0)
    test: int = Field(gt=0)
    stratified: bool


class CnnDatasetResource(StrictResource):
    name: str
    version: str
    source: str
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    classes: list[str] = Field(min_length=10, max_length=10)
    available_samples: int = Field(gt=0)
    image_shape: list[int] = Field(min_length=3, max_length=3)
    split: CnnDatasetSplitResource


class CnnPreprocessingResource(StrictResource):
    color_mode: str
    image_size: list[int] | tuple[int, int]
    value_range: list[float] | tuple[float, float]
    resize_policy: str
    normalization: str
    mean: float
    std: float = Field(gt=0.0)


class CnnLayerResource(StrictResource):
    id: str
    label: str
    operation: str
    channels: int = Field(gt=0)
    tensor_shape: list[int] = Field(min_length=4, max_length=4)


class CnnClassMetricResource(StrictResource):
    class_index: int = Field(ge=0, le=9)
    class_name: str
    correct: int = Field(ge=0)
    total: int = Field(gt=0)
    accuracy: float = Field(ge=0.0, le=1.0)


class CnnEvaluationResource(StrictResource):
    samples: int = Field(gt=0)
    loss: float = Field(ge=0.0)
    accuracy: float = Field(ge=0.0, le=1.0)
    correct: int = Field(ge=0)
    confusion_matrix: list[list[int]] = Field(min_length=10, max_length=10)
    per_class: list[CnnClassMetricResource] = Field(min_length=10, max_length=10)


class CnnVisualContractResource(StrictResource):
    transport: str
    normalization: str
    display_scale: list[float] = Field(min_length=2, max_length=2)
    maximum_channels_per_request: int = Field(gt=0)


class CnnSummaryResource(StrictResource):
    schema_version: str
    module: str
    status: str
    model: CnnModelResource
    dataset: CnnDatasetResource
    preprocessing: CnnPreprocessingResource
    layers: list[CnnLayerResource] = Field(min_length=1)
    evaluation: CnnEvaluationResource
    visual_contract: CnnVisualContractResource
    limitations: list[str] = Field(min_length=1)


class CnnSampleResource(StrictResource):
    id: str
    source_index: int = Field(ge=0)
    label_index: int = Field(ge=0, le=9)
    label: str
    image_data_uri: str = Field(pattern=r"^data:image/png;base64,")


class CnnSamplesResource(StrictResource):
    schema_version: str
    module: str
    samples: list[CnnSampleResource] = Field(min_length=10, max_length=10)


class CnnInputResource(StrictResource):
    source: str
    sample_id: str | None = None
    source_index: int | None = Field(default=None, ge=0)
    registered_label: str | None = None
    original_shape: list[int] = Field(min_length=2, max_length=2)
    tensor_shape: list[int] = Field(min_length=4, max_length=4)
    preprocessing: CnnPreprocessingResource
    image_data_uri: str = Field(pattern=r"^data:image/png;base64,")


class CnnProbabilityResource(StrictResource):
    class_index: int = Field(ge=0, le=9)
    class_name: str
    probability: float = Field(ge=0.0, le=1.0)


class CnnPredictionSummaryResource(StrictResource):
    predicted_index: int = Field(ge=0, le=9)
    predicted_class: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: list[CnnProbabilityResource] = Field(min_length=10, max_length=10)


class CnnPredictionResource(StrictResource):
    schema_version: str
    module: str
    model_version: str
    input: CnnInputResource
    prediction: CnnPredictionSummaryResource


class CnnFeatureMapResource(StrictResource):
    layer: str
    layer_label: str
    operation: str
    channel: int = Field(ge=0)
    tensor_shape: list[int] = Field(min_length=4, max_length=4)
    map_shape: list[int] = Field(min_length=2, max_length=2)
    raw_min: float
    raw_max: float
    raw_mean: float
    raw_std: float = Field(ge=0.0)
    normalization: str
    display_scale: list[float] = Field(min_length=2, max_length=2)
    values: list[list[float]] = Field(min_length=1)


class CnnRepresentationResource(StrictResource):
    layer: CnnLayerResource
    activation_tensor_shape: list[int] = Field(min_length=4, max_length=4)
    maps: list[CnnFeatureMapResource] = Field(min_length=1)
    comparison_rule: str


class CnnFeatureMapsResource(CnnPredictionResource):
    representation: CnnRepresentationResource
