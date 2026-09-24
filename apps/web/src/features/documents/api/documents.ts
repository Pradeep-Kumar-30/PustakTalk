import { api } from "@/lib/api/client";
import type { Document } from "@/types/api";

export function listDocuments(workspaceId: string) { return api<Document[]>(`/workspaces/${workspaceId}/documents`); }
export function uploadDocument(workspaceId: string, file: File) { const data = new FormData(); data.append("file", file); return api<Document>(`/workspaces/${workspaceId}/documents`, { method: "POST", body: data }); }
export function documentDownload(documentId: string) { return api<{ url: string }>(`/documents/${documentId}/download`); }

