export type DocumentStatus = "uploaded" | "processing" | "ready" | "failed";

export interface User { id: string; email: string; display_name: string; created_at: string }
export interface Workspace { id: string; name: string; description: string | null; created_at: string }
export interface Document { id: string; workspace_id: string; original_filename: string; status: DocumentStatus; page_count: number | null; failure_reason: string | null; created_at: string }
export interface Citation { id: string; document_id: string; document_name: string; chunk_id: string; physical_page: number; logical_page: string | null; source_text: string; bbox: number[] | null }
export interface ChatResponse { conversation_id: string; message_id: string; intent: string; answer: string; citations: Citation[]; grounded: boolean; created_at: string }

