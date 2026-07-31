import type {
  ForwardTrace,
  NeuralNetworkSummary,
  TrainingHistory
} from "@/types/neural-network";
import type {
  CnnFeatureMaps,
  CnnSamples,
  CnnSummary
} from "@/types/cnn";
import type {
  AutoencoderInterpolation,
  AutoencoderLatentPoints,
  AutoencoderReconstruction,
  AutoencoderSamples,
  AutoencoderSummary
} from "@/types/autoencoder";

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

export const imageDataUri =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=";

export const cnnSummaryFixture: CnnSummary = {
  schema_version: "1.0",
  module: "cnn-feature-map-viewer",
  status: "available",
  model: {
    name: "Fashion CNN",
    version: "fashion-cnn-v1",
    framework: "PyTorch 2.9.0+cpu",
    architecture: "Conv-BN-ReLU-Pool ×2 → Dense(128) → 10 classes",
    parameter_count: 207018,
    input_shape: [1, 28, 28],
    output_shape: [10],
    dataset: "fashion-mnist-official-sprite-900-v1",
    checkpoint: {
      file: "fashion-cnn-v1.pt",
      sha256: "b".repeat(64),
      bytes: 835989
    }
  },
  dataset: {
    name: "Fashion-MNIST",
    version: "fashion-mnist-official-sprite-900-v1",
    source: "official Fashion-MNIST sprite",
    source_sha256: "a".repeat(64),
    classes: [
      "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
      "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
    ],
    available_samples: 900,
    image_shape: [1, 28, 28],
    split: { training: 600, validation: 150, test: 150, stratified: true }
  },
  preprocessing: {
    color_mode: "grayscale",
    image_size: [28, 28],
    value_range: [0, 1],
    resize_policy: "bilinear-to-28x28",
    normalization: "(pixel-mean)/std",
    mean: 0.2860406,
    std: 0.35302424
  },
  layers: [
    {
      id: "block1_relu",
      label: "Edge and contour bank",
      operation: "Conv2d 3x3 + BatchNorm2d + ReLU",
      channels: 16,
      tensor_shape: [1, 16, 28, 28]
    },
    {
      id: "block2_relu",
      label: "Composed texture bank",
      operation: "Conv2d 3x3 + BatchNorm2d + ReLU after 2x2 max pooling",
      channels: 32,
      tensor_shape: [1, 32, 14, 14]
    }
  ],
  evaluation: {
    samples: 150,
    loss: 0.669677,
    accuracy: 0.8133333325,
    correct: 122,
    confusion_matrix: Array.from({ length: 10 }, () => Array(10).fill(0)),
    per_class: Array.from({ length: 10 }, (_, index) => ({
      class_index: index,
      class_name: `Class ${index}`,
      correct: 12,
      total: 15,
      accuracy: 0.8
    }))
  },
  visual_contract: {
    transport: "bounded-json-matrix",
    normalization: "per-channel-min-max-for-display",
    display_scale: [0, 1],
    maximum_channels_per_request: 12
  },
  limitations: [
    "Feature maps expose intermediate activations, not causal explanations.",
    "Each channel is normalized independently for display.",
    "The release uses a curated 900-image official sprite."
  ]
};

export const cnnSamplesFixture: CnnSamples = {
  schema_version: "1.0",
  module: "cnn-feature-map-viewer",
  samples: Array.from({ length: 10 }, (_, index) => ({
    id: `fashion-0${index}`,
    source_index: index * 90,
    label_index: index,
    label: cnnSummaryFixture.dataset.classes[index],
    image_data_uri: imageDataUri
  }))
};

export const cnnFeatureMapsFixture: CnnFeatureMaps = {
  schema_version: "1.0",
  module: "cnn-feature-map-viewer",
  model_version: "fashion-cnn-v1",
  input: {
    source: "registered-sample",
    sample_id: "fashion-08",
    source_index: 720,
    registered_label: "Bag",
    original_shape: [28, 28],
    tensor_shape: [1, 1, 28, 28],
    preprocessing: cnnSummaryFixture.preprocessing,
    image_data_uri: imageDataUri
  },
  prediction: {
    predicted_index: 8,
    predicted_class: "Bag",
    confidence: 0.947,
    probabilities: cnnSummaryFixture.dataset.classes.map((className, index) => ({
      class_index: index,
      class_name: className,
      probability: index === 8 ? 0.947 : 0.053 / 9
    }))
  },
  representation: {
    layer: cnnSummaryFixture.layers[0],
    activation_tensor_shape: [1, 16, 28, 28],
    maps: [0, 1, 2, 3, 4, 5].map((channel) => ({
      layer: "block1_relu",
      layer_label: "Edge and contour bank",
      operation: "Conv2d 3x3 + BatchNorm2d + ReLU",
      channel,
      tensor_shape: [1, 16, 28, 28],
      map_shape: [2, 2],
      raw_min: 0,
      raw_max: 1.2,
      raw_mean: 0.5,
      raw_std: 0.3,
      normalization: "per-channel-min-max-for-display",
      display_scale: [0, 1],
      values: [[0, 0.4], [0.7, 1]]
    })),
    comparison_rule:
      "Compare spatial patterns only. Each channel uses an independent display scale."
  }
};

export const autoencoderSummaryFixture: AutoencoderSummary = {
  schema_version: "1.0",
  module: "autoencoder-latent-space-demo",
  status: "available",
  model: {
    name: "Fashion convolutional autoencoder",
    version: "fashion-autoencoder-2d-v1",
    framework: "PyTorch 2.9.0+cpu",
    architecture: "Convolutional encoder → Latent(2) → convolutional decoder",
    parameter_count: 215923,
    input_shape: [1, 28, 28],
    latent_shape: [2],
    output_shape: [1, 28, 28],
    dataset: "fashion-mnist-official-sprite-900-v1",
    checkpoint: {
      file: "fashion-autoencoder-2d-v1.pt",
      sha256: "c".repeat(64),
      bytes: 875000
    }
  },
  dataset: cnnSummaryFixture.dataset,
  preprocessing: {
    color_mode: "grayscale",
    image_size: [28, 28],
    value_range: [0, 1],
    normalization: "pixel-divided-by-255",
    reconstruction_output: "sigmoid-bounded-0-to-1"
  },
  evaluation: {
    samples: 150,
    mean_squared_error: 0.033027,
    mean_absolute_error: 0.106527,
    pixels_evaluated: 117600
  },
  latent_contract: {
    dimensions: 2,
    distance: "euclidean-in-registered-2d-bottleneck",
    bounds: { x: [-4, 4], y: [-4, 4] },
    reference_points: 100,
    neighbors_returned: 5,
    interpolation: "linear-coordinate-segment-decoded-by-registered-model",
    minimum_steps: 3,
    maximum_steps: 12
  },
  limitations: [
    "The two-dimensional bottleneck sacrifices reconstruction capacity.",
    "Latent proximity does not guarantee universal semantic similarity.",
    "A smooth interpolation does not demonstrate understanding or causality.",
    "Fashion-MNIST is an educational benchmark."
  ]
};

const autoencoderPoints = Array.from({ length: 10 }, (_, index) => ({
  id: `latent-${String(index).padStart(2, "0")}-00`,
  source_index: index * 90,
  label_index: index,
  label: cnnSummaryFixture.dataset.classes[index],
  coordinate: [index - 4.5, (index % 3) - 1] as [number, number],
  reconstruction_error: 0.02 + index / 1000,
  image_data_uri: imageDataUri
}));

export const autoencoderSamplesFixture: AutoencoderSamples = {
  schema_version: "1.0",
  module: "autoencoder-latent-space-demo",
  samples: autoencoderPoints
};

export const autoencoderLatentPointsFixture: AutoencoderLatentPoints = {
  schema_version: "1.0",
  module: "autoencoder-latent-space-demo",
  model_version: "fashion-autoencoder-2d-v1",
  bounds: { x: [-5, 5], y: [-3, 3] },
  points: autoencoderPoints,
  interpretation:
    "Coordinates and distances belong only to this registered two-dimensional bottleneck."
};

export const autoencoderReconstructionFixture: AutoencoderReconstruction = {
  schema_version: "1.0",
  module: "autoencoder-latent-space-demo",
  model_version: "fashion-autoencoder-2d-v1",
  sample: autoencoderPoints[8],
  original: {
    tensor_shape: [1, 1, 28, 28],
    image_data_uri: imageDataUri
  },
  reconstruction: {
    tensor_shape: [1, 1, 28, 28],
    image_data_uri: imageDataUri,
    mean_squared_error: 0.0312,
    mean_absolute_error: 0.1014
  },
  latent_coordinate: autoencoderPoints[8].coordinate,
  neighbors: autoencoderPoints.slice(0, 5).map((point, index) => ({
    ...point,
    distance: 0.2 + index * 0.1
  })),
  interpretation:
    "The reconstruction and error were produced by the registered encoder-decoder."
};

export const autoencoderInterpolationFixture: AutoencoderInterpolation = {
  schema_version: "1.0",
  module: "autoencoder-latent-space-demo",
  model_version: "fashion-autoencoder-2d-v1",
  start: autoencoderPoints[8],
  end: autoencoderPoints[9],
  steps: Array.from({ length: 7 }, (_, index) => ({
    index,
    alpha: index / 6,
    coordinate: [3.5 + index / 6, 1 - index / 6] as [number, number],
    image_data_uri: imageDataUri
  })),
  interpretation:
    "Every frame is decoded from a linear segment in this model's 2D bottleneck."
};
