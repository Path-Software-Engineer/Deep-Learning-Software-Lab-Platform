import { expect, test } from "@playwright/test";

test("runs and inspects a registered PyTorch forward trace", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: /Follow every signal/i })
  ).toBeVisible();
  await expect(page.getByText("Checkpoint connected")).toBeVisible();
  await page.getByRole("button", { name: "Toggle x1" }).click();
  await page.getByRole("button", { name: /Run forward pass/i }).click();
  await expect(page.getByText(/Signal flow · \[1, 1\]/)).toBeVisible();
  await expect(page.getByText("Inspectable does not mean causal.")).toBeVisible();
  expect(consoleErrors).toEqual([]);
});
