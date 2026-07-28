import { afterEach, describe, expect, it, vi } from "vitest";

import { cnnApi, LabApiError, neuralNetworkApi } from "@/lib/api-client";

import { cnnFeatureMapsFixture, traceFixture } from "./fixtures";

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

describe("cnnApi", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("requests a registered sample with a bounded layer and channel selection", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(cnnFeatureMapsFixture), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    const result = await cnnApi.featureMaps(
      { sampleId: "fashion-08" },
      "block1_relu",
      [0, 3]
    );

    expect(result.prediction.predicted_class).toBe("Bag");
    const [path, options] = fetchMock.mock.calls[0];
    const url = new URL(String(path), "http://localhost");
    expect(url.pathname).toBe("/api/v1/cnn/feature-maps");
    expect(url.searchParams.get("sample_id")).toBe("fashion-08");
    expect(url.searchParams.get("layer")).toBe("block1_relu");
    expect(url.searchParams.getAll("channels")).toEqual(["0", "3"]);
    expect(options).toEqual(expect.objectContaining({ method: "POST" }));
  });

  it("sends uploads as raw image bodies without adding a JSON content type", async () => {
    const file = new File(["image"], "fashion.png", { type: "image/png" });
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(cnnFeatureMapsFixture), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    await cnnApi.predict({ file });

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/cnn/predict",
      expect.objectContaining({
        method: "POST",
        body: file,
        headers: { "Content-Type": "image/png" }
      })
    );
  });
});
