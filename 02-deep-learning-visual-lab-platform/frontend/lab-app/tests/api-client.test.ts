import { afterEach, describe, expect, it, vi } from "vitest";

import { LabApiError, neuralNetworkApi } from "@/lib/api-client";

import { traceFixture } from "./fixtures";

describe("neuralNetworkApi", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("sends only the selected XOR inputs to the forward contract", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(traceFixture), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    const result = await neuralNetworkApi.forward([1, 0]);

    expect(result.prediction).toBe(1);
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/neural-network/forward",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ inputs: [1, 0] })
      })
    );
  });

  it("maps the typed API error without exposing an opaque body", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            error: {
              code: "validation_error",
              message: "The request does not match the published API contract.",
              details: []
            }
          }),
          { status: 422, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    await expect(neuralNetworkApi.forward([0, 1])).rejects.toEqual(
      expect.objectContaining<Partial<LabApiError>>({
        code: "validation_error",
        status: 422
      })
    );
  });
});
