export interface AutoencoderCheckpoint {
  file: string;
  sha256: string;
  bytes: number;
}

export interface LatentBounds {
  x: [number, number];
  y: [number, number];
}

export interface AutoencoderSummary {
  schema_version: string;
  module: string;
  status: string;
  model: {
    name: string;
    version: string;
    framework: string;
    architecture: string;
    parameter_count: number;
    input_shape: number[];
    latent_shape: number[];
    output_shape: number[];
    dataset: string;
    checkpoint: AutoencoderCheckpoint;
  };
  dataset: {
    name: string;
    version: string;
    source: string;
    source_sha256: string;
    classes: string[];
    available_samples: number;
    image_shape: number[];
    split: {
      training: number;
      validation: number;
      test: number;
      stratified: boolean;
    };
  };
  preprocessing: {
    color_mode: string;
    image_size: number[];
    value_range: number[];
    normalization: string;
    reconstruction_output: string;
  };
  evaluation: {
    samples: number;
    mean_squared_error: number;
    mean_absolute_error: number;
    pixels_evaluated: number;
  };
  latent_contract: {
    dimensions: 2;
    distance: string;
    bounds: LatentBounds;
    reference_points: number;
    neighbors_returned: number;
    interpolation: string;
    minimum_steps: number;
    maximum_steps: number;
  };
  limitations: string[];
}

export interface AutoencoderSample {
  id: string;
  source_index: number;
  label_index: number;
  label: string;
  coordinate: [number, number];
  reconstruction_error: number;
  image_data_uri: string;
}

export interface AutoencoderSamples {
  schema_version: string;
  module: string;
  samples: AutoencoderSample[];
}

export interface AutoencoderLatentPoints {
  schema_version: string;
  module: string;
  model_version: string;
  bounds: LatentBounds;
  points: AutoencoderSample[];
  interpretation: string;
}

export interface AutoencoderNeighbor extends AutoencoderSample {
  distance: number;
}

export interface AutoencoderReconstruction {
  schema_version: string;
  module: string;
  model_version: string;
  sample: AutoencoderSample;
  original: {
    tensor_shape: number[];
    image_data_uri: string;
  };
  reconstruction: {
    tensor_shape: number[];
    image_data_uri: string;
    mean_squared_error: number;
    mean_absolute_error: number;
  };
  latent_coordinate: [number, number];
  neighbors: AutoencoderNeighbor[];
  interpretation: string;
}

export interface AutoencoderInterpolationStep {
  index: number;
  alpha: number;
  coordinate: [number, number];
  image_data_uri: string;
}

export interface AutoencoderInterpolation {
  schema_version: string;
  module: string;
  model_version: string;
  start: AutoencoderSample;
  end: AutoencoderSample;
  steps: AutoencoderInterpolationStep[];
  interpretation: string;
}
