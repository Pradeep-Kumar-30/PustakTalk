import { api } from "@/lib/api/client";
import type { Workspace } from "@/types/api";

export function listWorkspaces() { return api<Workspace[]>("/workspaces"); }
export function createWorkspace(payload: { name: string; description?: string }) { return api<Workspace>("/workspaces", { method: "POST", body: JSON.stringify(payload) }); }

