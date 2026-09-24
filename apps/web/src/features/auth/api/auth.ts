import { api } from "@/lib/api/client";
import type { User } from "@/types/api";

export function register(payload: { email: string; password: string; display_name: string }) { return api<User>("/auth/register", { method: "POST", body: JSON.stringify(payload) }); }
export function login(payload: { email: string; password: string }) { return api<User>("/auth/login", { method: "POST", body: JSON.stringify(payload) }); }
export function currentUser() { return api<User>("/auth/me"); }
export function logout() { return api<void>("/auth/logout", { method: "POST" }); }

