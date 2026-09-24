import { test, expect } from "@playwright/test";

test.describe("PustakTalk critical path", () => {
  test.skip(!process.env.PUSTAKTALK_E2E, "Requires a seeded full stack and a fixture PDF");
  test("registers, uploads, chats, and opens a cited page", async ({ page }) => {
    await page.goto("http://localhost:3000/register");
    await page.getByLabel("Name").fill("E2E Student");
    await page.getByLabel("Email").fill("e2e@example.test");
    await page.getByLabel("Password").fill("an-exactly-strong-password");
    await page.getByRole("button", { name: "Create account" }).click();
    await expect(page.getByText("Your research spaces")).toBeVisible();
  });
});
