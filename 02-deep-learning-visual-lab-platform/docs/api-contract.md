# Versioned API Contract

Base URL: `/api/v1`.

## `GET /platform/modules`

Lists the modules currently available. Sprint 1 registers only
`neural-network-explainer`; Sprint 2 also registers
`cnn-feature-map-viewer`.

## `GET /neural-network/summary`

Returns:

- controlled dataset metadata;
- 2–4–1 architecture and activation names;
- parameter count;
- checkpoint filename, size and SHA-256;
- engine and limitations.

## `POST /neural-network/forward`

Request:

```json
{ "inputs": [0, 1] }
```

Both values must be binary. Unknown fields are rejected.

Response:

- validated inputs and XOR target;
- hidden and output layer weights and biases;
- preactivations and activations;
- probability, prediction, threshold and sample loss;
- model version and checkpoint checksum;
- limitations.

## `GET /neural-network/training-history`

Returns the recorded seed, optimizer, learning rate, epochs, loss function,
metrics and sampled loss points produced by offline training.

## Errors

Validation errors use the shared envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "The request does not match the published API contract.",
    "details": [{ "field": "inputs", "message": "..." }]
  }
}
```

The canonical generated schema is `docs/api/openapi.json`.

## `GET /cnn/summary`

Returns registered model, checkpoint, dataset provenance, preprocessing,
observable layers, held-out evaluation, display contract and limitations.

## `GET /cnn/samples`

Returns one allowlisted 28 × 28 sample for each official Fashion-MNIST class.

## `POST /cnn/predict`

Accepts either `sample_id` or a raw `image/png` / `image/jpeg` body. The inputs
are mutually exclusive. Uploads are bounded to 1 MiB and 1024 × 1024 pixels,
converted to grayscale, resized and never persisted.

## `POST /cnn/feature-maps`

Uses the same image input plus:

- `layer`: one published layer ID;
- `channels`: one to twelve unique channel indices.

Returns the prediction, tensor shape, selected maps, raw channel statistics and
display-only normalized matrices.
