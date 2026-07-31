import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { PlatformShell } from "@/components/platform/PlatformShell";

describe("PlatformShell", () => {
  afterEach(() => {
    cleanup();
  });

  it("keeps one ordered module navigation without section routes", () => {
    render(
      <PlatformShell
        activeModule="feature-maps"
        sprint="Sprint 02"
        title="CNN Feature Map Viewer"
        status="Checkpoint connected"
        version="fashion-cnn-v1"
      >
        <p>Module content</p>
      </PlatformShell>
    );

    const navigation = screen.getByRole("navigation", {
      name: "Platform modules"
    });
    const links = within(navigation).getAllByRole("link");

    expect(links).toHaveLength(3);
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      "/",
      "/cnn",
      "/autoencoder"
    ]);
    expect(links[1]).toHaveAccessibleName(/Feature maps.*Fashion CNN/i);
    expect(links[1]).toHaveAttribute("aria-current", "page");
    expect(
      links.some((link) => link.getAttribute("href")?.startsWith("#"))
    ).toBe(false);
  });

  it("offers a keyboard skip link to the stable module content", () => {
    render(
      <PlatformShell
        activeModule="latent-space"
        sprint="Sprint 03"
        title="Autoencoder Latent Space Demo"
        status="Checkpoint connected"
        version="fashion-autoencoder-2d-v1"
      >
        <p>Module content</p>
      </PlatformShell>
    );

    expect(
      screen.getByRole("link", { name: "Skip to module content" })
    ).toHaveAttribute("href", "#main-content");
    expect(screen.getByRole("main")).toHaveAttribute("id", "main-content");
  });
});
