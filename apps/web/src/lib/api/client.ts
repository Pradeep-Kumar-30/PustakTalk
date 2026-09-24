import { apiBaseUrl } from "@/config/env";

export class ApiError extends Error {
  constructor(message: string, public readonly status: number) { super(message); }
}

function errorMessage(body: unknown): string {
  if (typeof body !== "object" || body === null) return "Something went wrong";
  const problem = body as { detail?: unknown; error?: { message?: unknown } };
  if (typeof problem.detail === "string") return problem.detail;
  if (typeof problem.error?.message === "string") return problem.error.message;
  return "Something went wrong";
}

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    credentials: "include",
    headers: { ...(init.body instanceof FormData ? {} : { "Content-Type": "application/json" }), ...init.headers },
    ...init,
  });
  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    throw new ApiError(errorMessage(body), response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
