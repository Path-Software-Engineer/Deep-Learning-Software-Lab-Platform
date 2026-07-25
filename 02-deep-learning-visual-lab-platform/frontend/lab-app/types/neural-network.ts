export interface Checkpoint {
  file: string;
  sha256: string;
  bytes: number;
}

export interface NeuralNetworkSummary {
  module_id: string;
  name: string;
  status: "available";
  model_version: string;
  dataset: {
    name: string;
    description: string;
    samples: number;
    features: number;
    targets: number;
    points: number[][];
    labels: number[];
  };
  architecture: {
    input_nodes: number;
    hidden_nodes: number;
    output_nodes: number;
    hidden_activation: string;
    output_activation: string;
    parameter_count: number;
  };
  checkpoint: Checkpoint;
  engine: string;
  limitations: string[];
}

export interface LayerTrace {
  id: "hidden" | "output";
  label: string;
  operation: string;
  weights: number[][];
  biases: number[];
  preactivations: number[];
  activations: number[];
}

export interface ForwardTrace {
  inputs: [number, number];
  layers: [LayerTrace, LayerTrace];
  output: number;
  target: number;
  loss: number;
  prediction: 0 | 1;
  threshold: number;
  model_version: string;
  checkpoint_sha256: string;
  limitations: string[];
}

export interface TrainingPoint {
  epoch: number;
  loss: number;
}

export interface TrainingHistory {
  model_version: string;
  seed: number;
  configuration: {
    seed: number;
    epochs: number;
    learning_rate: number;
    optimizer: string;
    loss_function: string;
    history_interval: number;
    threshold: number;
  };
  metrics: {
    accuracy: number;
    final_loss: number;
  };
  points: TrainingPoint[];
  limitations: string[];
}

export interface ApiErrorEnvelope {
  error: {
    code: string;
    message: string;
    details: Array<{ field: string | null; message: string }>;
  };
}
