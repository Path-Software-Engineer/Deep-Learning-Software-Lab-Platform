import { expect, test } from "@playwright/test";

test("inspects registered Fashion-MNIST feature maps through the real API", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.goto("/cnn");
  await expect(
    page.getByRole("heading", { name: /See what each channel responds to/i })
  ).toBeVisible();
  await expect(page.getByText("Checkpoint connected")).toBeVisible();
  await expect(page.getByText("Activation is not explanation.")).toBeVisible();

  await page.getByRole("button", { name: /Composed texture bank/i }).click();
  await page.getByRole("button", { name: /Run feature-map inspection/i }).click();

  await expect(page.getByText("Composed texture bank").first()).toBeVisible();
  await expect(page.getByRole("img", { name: /channel 0, normalized/i })).toBeVisible();
  expect(consoleErrors).toEqual([]);
});
