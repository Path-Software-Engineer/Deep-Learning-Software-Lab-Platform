export interface CnnCheckpoint {
  file: string;
  sha256: string;
  bytes: number;
}

export interface CnnLayer {
  id: string;
  label: string;
  operation: string;
  channels: number;
  tensor_shape: number[];
}

export interface CnnClassMetric {
  class_index: number;
  class_name: string;
  correct: number;
  total: number;
  accuracy: number;
}

export interface CnnEvaluation {
  samples: number;
  loss: number;
  accuracy: number;
  correct: number;
  confusion_matrix: number[][];
  per_class: CnnClassMetric[];
}

export interface CnnSummary {
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
    output_shape: number[];
    dataset: string;
    checkpoint: CnnCheckpoint;
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
    resize_policy: string;
    normalization: string;
    mean: number;
    std: number;
  };
  layers: CnnLayer[];
  evaluation: CnnEvaluation;
  visual_contract: {
    transport: string;
    normalization: string;
    display_scale: number[];
    maximum_channels_per_request: number;
  };
  limitations: string[];
}

export interface CnnSample {
  id: string;
  source_index: number;
  label_index: number;
  label: string;
  image_data_uri: string;
}

export interface CnnSamples {
  schema_version: string;
  module: string;
  samples: CnnSample[];
}

export interface CnnInput {
  source: string;
  sample_id?: string;
  source_index?: number;
  registered_label?: string;
  original_shape: number[];
  tensor_shape: number[];
  preprocessing: CnnSummary["preprocessing"];
  image_data_uri: string;
}

export interface CnnProbability {
  class_index: number;
  class_name: string;
  probability: number;
}

export interface CnnPredictionSummary {
  predicted_index: number;
  predicted_class: string;
  confidence: number;
  probabilities: CnnProbability[];
}

export interface CnnPrediction {
  schema_version: string;
  module: string;
  model_version: string;
  input: CnnInput;
  prediction: CnnPredictionSummary;
}

export interface CnnFeatureMap {
  layer: string;
  layer_label: string;
  operation: string;
  channel: number;
  tensor_shape: number[];
  map_shape: number[];
  raw_min: number;
  raw_max: number;
  raw_mean: number;
  raw_std: number;
  normalization: string;
  display_scale: number[];
  values: number[][];
}

export interface CnnFeatureMaps extends CnnPrediction {
  representation: {
    layer: CnnLayer;
    activation_tensor_shape: number[];
    maps: CnnFeatureMap[];
    comparison_rule: string;
  };
}

export interface CnnImageInput {
  sampleId?: string;
  file?: File;
}
