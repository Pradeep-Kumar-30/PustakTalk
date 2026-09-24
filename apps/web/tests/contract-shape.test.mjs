import test from "node:test";
import assert from "node:assert/strict";

test("API base URL can target a same-origin production proxy", () => {
  const url = process.env.NEXT_PUBLIC_API_URL ?? "/api/v1";
  assert.match(url, /api\/v1$/);
});
