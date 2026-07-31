import type {
  ApiErrorEnvelope,
  ForwardTrace,
  NeuralNetworkSummary,
  TrainingHistory
} from "@/types/neural-network";
import type {
  CnnFeatureMaps,
  CnnImageInput,
  CnnPrediction,
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

const API_ROOT = (
  process.env.NEXT_PUBLIC_API_ROOT ?? ""
).replace(/\/$/, "");
const REQUEST_TIMEOUT_MS = 10_000;

export class LabApiError extends Error {
  constructor(
    message: string,
    readonly code: string,
    readonly status: number
  ) {
    super(message);
    this.name = "LabApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_ROOT}${path}`, {
      ...init,
      cache: "no-store",
      signal: init?.signal ?? AbortSignal.timeout(REQUEST_TIMEOUT_MS),
      headers: {
        ...(typeof init?.body === "string"
          ? { "Content-Type": "application/json" }
          : {}),
        ...init?.headers
      }
    });
  } catch {
    throw new LabApiError(
      "The lab engine is unreachable. Start FastAPI and retry.",
      "network_unavailable",
      0
    );
  }
  if (!response.ok) {
    let message = `The API returned ${response.status}.`;
    let code = "api_error";
    try {
      const resource = (await response.json()) as ApiErrorEnvelope;
      message = resource.error.message;
      code = resource.error.code;
    } catch {
      // The safe fallback intentionally avoids exposing an opaque response body.
    }
    throw new LabApiError(message, code, response.status);
  }
  return (await response.json()) as T;
}

export const neuralNetworkApi = {
  summary: () =>
    request<NeuralNetworkSummary>("/api/v1/neural-network/summary"),
  trainingHistory: () =>
    request<TrainingHistory>("/api/v1/neural-network/training-history"),
  forward: (inputs: [number, number]) =>
    request<ForwardTrace>("/api/v1/neural-network/forward", {
      method: "POST",
      body: JSON.stringify({ inputs })
    })
};

function cnnInputRequest(
  path: string,
  input: CnnImageInput,
): RequestInit & { path: string } {
  const query = new URLSearchParams();
  if (input.sampleId) query.set("sample_id", input.sampleId);
  const suffix = query.size ? `?${query.toString()}` : "";
  return {
    path: `${path}${suffix}`,
    method: "POST",
    body: input.file,
    headers: input.file ? { "Content-Type": input.file.type } : undefined
  };
}

export const cnnApi = {
  summary: () => request<CnnSummary>("/api/v1/cnn/summary"),
  samples: () => request<CnnSamples>("/api/v1/cnn/samples"),
  predict: (input: CnnImageInput) => {
    const { path, ...init } = cnnInputRequest("/api/v1/cnn/predict", input);
    return request<CnnPrediction>(path, init);
  },
  featureMaps: (
    input: CnnImageInput,
    layer: string,
    channels: number[]
  ) => {
    const prepared = cnnInputRequest("/api/v1/cnn/feature-maps", input);
    const [base, existing = ""] = prepared.path.split("?");
    const query = new URLSearchParams(existing);
    query.set("layer", layer);
    channels.forEach((channel) => query.append("channels", String(channel)));
    const { path: _, ...init } = prepared;
    void _;
    return request<CnnFeatureMaps>(`${base}?${query.toString()}`, init);
  }
};

export const autoencoderApi = {
  summary: () =>
    request<AutoencoderSummary>("/api/v1/autoencoder/summary"),
  samples: () =>
    request<AutoencoderSamples>("/api/v1/autoencoder/samples"),
  latentPoints: () =>
    request<AutoencoderLatentPoints>("/api/v1/autoencoder/latent-points"),
  reconstruct: (pointId: string) =>
    request<AutoencoderReconstruction>("/api/v1/autoencoder/reconstruct", {
      method: "POST",
      body: JSON.stringify({ point_id: pointId })
    }),
  interpolate: (startId: string, endId: string, steps: number) =>
    request<AutoencoderInterpolation>("/api/v1/autoencoder/interpolate", {
      method: "POST",
      body: JSON.stringify({
        start_id: startId,
        end_id: endId,
        steps
      })
    })
};
