"""Pydantic resources for the public Sprint 3 autoencoder contract."""

from __future__ import annotations

from pydantic import Field

from app.common.resources import StrictResource


class AutoencoderCheckpointResource(StrictResource):
    file: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    bytes: int = Field(gt=0)


class AutoencoderModelResource(StrictResource):
    name: str
    version: str
    framework: str
    architecture: str
    parameter_count: int = Field(gt=0)
    input_shape: list[int] = Field(min_length=3, max_length=3)
    latent_shape: list[int] = Field(min_length=1, max_length=1)
    output_shape: list[int] = Field(min_length=3, max_length=3)
    dataset: str
    checkpoint: AutoencoderCheckpointResource


class AutoencoderDatasetSplitResource(StrictResource):
    training: int = Field(gt=0)
    validation: int = Field(gt=0)
    test: int = Field(gt=0)
    stratified: bool


class AutoencoderDatasetResource(StrictResource):
    name: str
    version: str
    source: str
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    classes: list[str] = Field(min_length=10, max_length=10)
    available_samples: int = Field(gt=0)
    image_shape: list[int] = Field(min_length=3, max_length=3)
    split: AutoencoderDatasetSplitResource


class AutoencoderPreprocessingResource(StrictResource):
    color_mode: str
    image_size: list[int] | tuple[int, int]
    value_range: list[float] | tuple[float, float]
    normalization: str
    reconstruction_output: str


class AutoencoderEvaluationResource(StrictResource):
    samples: int = Field(gt=0)
    mean_squared_error: float = Field(ge=0.0)
    mean_absolute_error: float = Field(ge=0.0)
    pixels_evaluated: int = Field(gt=0)


class LatentBoundsResource(StrictResource):
    x: list[float] = Field(min_length=2, max_length=2)
    y: list[float] = Field(min_length=2, max_length=2)


class LatentContractResource(StrictResource):
    dimensions: int = Field(ge=2, le=2)
    distance: str
    bounds: LatentBoundsResource
    reference_points: int = Field(gt=0)
    neighbors_returned: int = Field(gt=0)
    interpolation: str
    minimum_steps: int = Field(ge=2)
    maximum_steps: int = Field(ge=3)


class AutoencoderSummaryResource(StrictResource):
    schema_version: str
    module: str
    status: str
    model: AutoencoderModelResource
    dataset: AutoencoderDatasetResource
    preprocessing: AutoencoderPreprocessingResource
    evaluation: AutoencoderEvaluationResource
    latent_contract: LatentContractResource
    limitations: list[str] = Field(min_length=1)


class AutoencoderSampleResource(StrictResource):
    id: str
    source_index: int = Field(ge=0)
    label_index: int = Field(ge=0, le=9)
    label: str
    coordinate: list[float] = Field(min_length=2, max_length=2)
    reconstruction_error: float = Field(ge=0.0)
    image_data_uri: str = Field(pattern=r"^data:image/png;base64,")


class AutoencoderSamplesResource(StrictResource):
    schema_version: str
    module: str
    samples: list[AutoencoderSampleResource] = Field(min_length=10, max_length=10)


class AutoencoderLatentPointsResource(StrictResource):
    schema_version: str
    module: str
    model_version: str
    bounds: LatentBoundsResource
    points: list[AutoencoderSampleResource] = Field(min_length=1)
    interpretation: str


class AutoencoderReconstructRequest(StrictResource):
    point_id: str = Field(min_length=1, max_length=64)


class AutoencoderImageResource(StrictResource):
    tensor_shape: list[int] = Field(min_length=4, max_length=4)
    image_data_uri: str = Field(pattern=r"^data:image/png;base64,")


class AutoencoderReconstructedImageResource(AutoencoderImageResource):
    mean_squared_error: float = Field(ge=0.0)
    mean_absolute_error: float = Field(ge=0.0)


class AutoencoderNeighborResource(AutoencoderSampleResource):
    distance: float = Field(ge=0.0)


class AutoencoderReconstructionResource(StrictResource):
    schema_version: str
    module: str
    model_version: str
    sample: AutoencoderSampleResource
    original: AutoencoderImageResource
    reconstruction: AutoencoderReconstructedImageResource
    latent_coordinate: list[float] = Field(min_length=2, max_length=2)
    neighbors: list[AutoencoderNeighborResource] = Field(min_length=1)
    interpretation: str


class AutoencoderInterpolationRequest(StrictResource):
    start_id: str = Field(min_length=1, max_length=64)
    end_id: str = Field(min_length=1, max_length=64)
    steps: int = Field(ge=3, le=12)


class AutoencoderInterpolationStepResource(StrictResource):
    index: int = Field(ge=0)
    alpha: float = Field(ge=0.0, le=1.0)
    coordinate: list[float] = Field(min_length=2, max_length=2)
    image_data_uri: str = Field(pattern=r"^data:image/png;base64,")


class AutoencoderInterpolationResource(StrictResource):
    schema_version: str
    module: str
    model_version: str
    start: AutoencoderSampleResource
    end: AutoencoderSampleResource
    steps: list[AutoencoderInterpolationStepResource] = Field(min_length=3, max_length=12)
    interpretation: str
