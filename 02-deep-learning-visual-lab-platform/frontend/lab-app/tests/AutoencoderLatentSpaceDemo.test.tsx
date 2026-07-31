import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { AutoencoderLatentSpaceDemo } from "@/features/autoencoder/components/AutoencoderLatentSpaceDemo";

import {
  autoencoderInterpolationFixture,
  autoencoderLatentPointsFixture,
  autoencoderReconstructionFixture,
  autoencoderSamplesFixture,
  autoencoderSummaryFixture
} from "./fixtures";

function jsonResponse(value: unknown) {
  return new Response(JSON.stringify(value), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}

describe("AutoencoderLatentSpaceDemo", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn()
        .mockResolvedValueOnce(jsonResponse(autoencoderSummaryFixture))
        .mockResolvedValueOnce(jsonResponse(autoencoderSamplesFixture))
        .mockResolvedValueOnce(jsonResponse(autoencoderLatentPointsFixture))
        .mockResolvedValueOnce(jsonResponse(autoencoderReconstructionFixture))
        .mockResolvedValueOnce(jsonResponse(autoencoderInterpolationFixture))
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("renders reconstruction, latent points, neighbors and evidence limits", async () => {
    render(<AutoencoderLatentSpaceDemo />);

    expect(
      screen.getByText(/Loading registered reconstruction evidence/)
    ).toBeInTheDocument();
    expect(
      await screen.findByRole("heading", {
        name: "Compare source and reconstruction."
      })
    ).toBeInTheDocument();
    expect(screen.getByText("0.031200")).toBeInTheDocument();
    expect(
      screen.getByRole("group", {
        name: "Registered two-dimensional latent reference points"
      })
    ).toBeInTheDocument();
    expect(screen.getByText("Nearest registered points")).toBeInTheDocument();
    expect(
      screen.getByText(/does not demonstrate understanding or causality/)
    ).toBeInTheDocument();
  });

  it("requests a new reconstruction when a registered sample is selected", async () => {
    render(<AutoencoderLatentSpaceDemo />);
    await screen.findByText("0.031200");
    vi.mocked(fetch).mockResolvedValueOnce(
      jsonResponse({
        ...autoencoderReconstructionFixture,
        sample: autoencoderSamplesFixture.samples[1],
        latent_coordinate: autoencoderSamplesFixture.samples[1].coordinate
      })
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Trouser registered sample/i })
    );

    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(6));
    const [path, options] = vi.mocked(fetch).mock.calls[5];
    expect(path).toBe("/api/v1/autoencoder/reconstruct");
    expect(options).toEqual(
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ point_id: "latent-01-00" })
      })
    );
  });
});
