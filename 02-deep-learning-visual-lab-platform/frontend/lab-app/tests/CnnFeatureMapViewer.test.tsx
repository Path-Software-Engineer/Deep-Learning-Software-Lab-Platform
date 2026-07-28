import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { CnnFeatureMapViewer } from "@/features/cnn/components/CnnFeatureMapViewer";

import {
  cnnFeatureMapsFixture,
  cnnSamplesFixture,
  cnnSummaryFixture
} from "./fixtures";

function jsonResponse(value: unknown) {
  return new Response(JSON.stringify(value), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}

describe("CnnFeatureMapViewer", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn()
        .mockResolvedValueOnce(jsonResponse(cnnSummaryFixture))
        .mockResolvedValueOnce(jsonResponse(cnnSamplesFixture))
        .mockResolvedValueOnce(jsonResponse(cnnFeatureMapsFixture))
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("renders registered prediction, tensor metadata, maps and limitations", async () => {
    render(<CnnFeatureMapViewer />);

    expect(screen.getByText(/Loading registered Fashion-MNIST evidence/)).toBeInTheDocument();
    expect((await screen.findAllByText("94.7%")).length).toBeGreaterThanOrEqual(1);
    expect(
      screen.getByRole("heading", { name: "Edge and contour bank" })
    ).toBeInTheDocument();
    expect(screen.getAllByRole("img", { name: /normalized feature map/i })).toHaveLength(6);
    expect(screen.getByText("Activation is not explanation.")).toBeInTheDocument();
    expect(screen.getByText(/curated 900-image official sprite/)).toBeInTheDocument();
  });

  it("requests the selected layer and channels from FastAPI", async () => {
    render(<CnnFeatureMapViewer />);
    await screen.findAllByText("94.7%");
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(jsonResponse({
      ...cnnFeatureMapsFixture,
      representation: {
        ...cnnFeatureMapsFixture.representation,
        layer: cnnSummaryFixture.layers[1],
        activation_tensor_shape: [1, 32, 14, 14]
      }
    }));

    fireEvent.click(screen.getByRole("button", { name: /Composed texture bank/i }));
    fireEvent.click(screen.getByRole("button", { name: "05" }));
    fireEvent.click(screen.getByRole("button", { name: /Run feature-map inspection/i }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    const [path] = fetchMock.mock.calls[3];
    const url = new URL(String(path), "http://localhost");
    expect(url.searchParams.get("layer")).toBe("block2_relu");
    expect(url.searchParams.getAll("channels")).toEqual(["0", "1", "2", "3", "4"]);
  });

  it("requires a file before an upload inspection can run", async () => {
    render(<CnnFeatureMapViewer />);
    await screen.findAllByText("94.7%");

    fireEvent.click(screen.getByRole("tab", { name: "Temporary upload" }));
    fireEvent.click(screen.getByRole("button", { name: /Run feature-map inspection/i }));

    expect(screen.getByRole("alert")).toHaveTextContent(
      "Choose a PNG or JPEG image before running the inspection."
    );
    expect(fetch).toHaveBeenCalledTimes(3);
  });
});
