import { expect, test } from "@playwright/test";

test("explores registered reconstructions and decoder interpolation", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.goto("/autoencoder");
  await expect(
    page.getByRole("heading", { name: /Compress the image/i })
  ).toBeVisible();
  await expect(page.getByText("Checkpoint connected")).toBeVisible();
  await expect(page.getByText(/2D bottleneck sacrifices capacity/i)).toBeVisible();

  await page.getByRole("button", { name: /Bag/i }).first().click();
  await expect(page.getByRole("img", { name: /Reconstructed Bag/i })).toBeVisible();

  await page.getByRole("button", { name: /Decode interpolation/i }).click();
  await expect(page.getByText(/PyTorch decodes every/i)).toBeVisible();
  await expect(page.getByRole("img", { name: /Decoded interpolation/i })).toHaveCount(7);
  expect(consoleErrors).toEqual([]);
});
