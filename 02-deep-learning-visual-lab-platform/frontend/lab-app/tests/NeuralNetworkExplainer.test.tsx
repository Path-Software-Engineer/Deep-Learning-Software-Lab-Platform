import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { NeuralNetworkExplainer } from "@/features/neural-network/components/NeuralNetworkExplainer";

import { historyFixture, summaryFixture, traceFixture } from "./fixtures";

function jsonResponse(value: unknown) {
  return new Response(JSON.stringify(value), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}

describe("NeuralNetworkExplainer", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn()
        .mockResolvedValueOnce(jsonResponse(summaryFixture))
        .mockResolvedValueOnce(jsonResponse(historyFixture))
        .mockResolvedValueOnce(jsonResponse(traceFixture))
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("renders registered prediction, trace and limitations", async () => {
    render(<NeuralNetworkExplainer />);
    expect(screen.getByText(/Loading registered PyTorch evidence/)).toBeInTheDocument();
    expect(await screen.findByText("96.08%")).toBeInTheDocument();
    expect(
      screen.getByRole("img", { name: /interactive two-layer neural network/i })
    ).toBeInTheDocument();
    expect(screen.getByText("Inspectable does not mean causal.")).toBeInTheDocument();
    expect(screen.getByText(/Activations are internal representations/)).toBeInTheDocument();
  });

  it("requests a forward pass for the selected binary inputs", async () => {
    render(<NeuralNetworkExplainer />);
    await screen.findByText("96.08%");
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({ ...traceFixture, inputs: [1, 1], output: 0.001, prediction: 0, target: 0 })
    );

    fireEvent.click(screen.getByRole("button", { name: "Toggle x1" }));
    fireEvent.click(screen.getByRole("button", { name: /Run forward pass/i }));

    await waitFor(() => expect(screen.getByText("0.10%")).toBeInTheDocument());
    expect(fetchMock).toHaveBeenLastCalledWith(
      "/api/v1/neural-network/forward",
      expect.objectContaining({ body: JSON.stringify({ inputs: [1, 1] }) })
    );
  });
});
