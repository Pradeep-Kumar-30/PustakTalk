import { api } from "@/lib/api/client";
import type { ChatResponse } from "@/types/api";

export function sendChat(payload: { workspace_id: string; question: string; conversation_id?: string; document_ids?: string[] }) { return api<ChatResponse>("/chat", { method: "POST", body: JSON.stringify(payload) }); }

