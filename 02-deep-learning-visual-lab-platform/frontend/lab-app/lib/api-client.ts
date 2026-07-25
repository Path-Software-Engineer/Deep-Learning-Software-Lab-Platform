import type {
  ApiErrorEnvelope,
  ForwardTrace,
  NeuralNetworkSummary,
  TrainingHistory
} from "@/types/neural-network";

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
        "Content-Type": "application/json",
        ...init?.headers
      }
    });
  } catch {
    throw new LabApiError(
      "The neural engine is unreachable. Start FastAPI and retry.",
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
