import type {
  ForwardTrace,
  NeuralNetworkSummary,
  TrainingHistory
} from "@/types/neural-network";

export const summaryFixture: NeuralNetworkSummary = {
  module_id: "neural-network-explainer",
  name: "Neural Network Explainer",
  status: "available",
  model_version: "xor-mlp-v1",
  dataset: {
    name: "xor",
    description: "Controlled binary XOR truth table.",
    samples: 4,
    features: 2,
    targets: 1,
    points: [[0, 0], [0, 1], [1, 0], [1, 1]],
    labels: [0, 1, 1, 0]
  },
  architecture: {
    input_nodes: 2,
    hidden_nodes: 4,
    output_nodes: 1,
    hidden_activation: "tanh",
    output_activation: "sigmoid",
    parameter_count: 17
  },
  checkpoint: { file: "xor-mlp-v1.pt", sha256: "a".repeat(64), bytes: 2875 },
  engine: "PyTorch",
  limitations: [
    "XOR is a four-observation educational dataset, not a production benchmark.",
    "Training accuracy is not a generalization claim.",
    "Activations are internal representations, not causal explanations."
  ]
};

export const traceFixture: ForwardTrace = {
  inputs: [0, 1],
  layers: [
    {
      id: "hidden",
      label: "Hidden layer",
      operation: "Linear + tanh",
      weights: [[0.1, 0.2], [0.3, -0.4], [0.5, 0.6], [-0.7, 0.8]],
      biases: [0.1, 0.2, 0.3, 0.4],
      preactivations: [0.3, -0.2, 0.9, 1.2],
      activations: [0.291, -0.197, 0.716, 0.834]
    },
    {
      id: "output",
      label: "Output layer",
      operation: "Linear + sigmoid",
      weights: [[0.4, -0.2, 0.6, 0.8]],
      biases: [0.1],
      preactivations: [3.2],
      activations: [0.9608]
    }
  ],
  output: 0.9608,
  target: 1,
  loss: 0.04,
  prediction: 1,
  threshold: 0.5,
  model_version: "xor-mlp-v1",
  checkpoint_sha256: "a".repeat(64),
  limitations: summaryFixture.limitations
};

export const historyFixture: TrainingHistory = {
  model_version: "xor-mlp-v1",
  seed: 190,
  configuration: {
    seed: 190,
    epochs: 2000,
    learning_rate: 0.05,
    optimizer: "Adam",
    loss_function: "BCELoss",
    history_interval: 10,
    threshold: 0.5
  },
  metrics: { accuracy: 1, final_loss: 0.00005 },
  points: [
    { epoch: 0, loss: 0.72 },
    { epoch: 1000, loss: 0.01 },
    { epoch: 2000, loss: 0.00005 }
  ],
  limitations: summaryFixture.limitations
};
