export type DocumentStatus = "uploaded" | "processing" | "ready" | "failed";

export interface DocumentContract {
  id: string;
  workspace_id: string;
  original_filename: string;
  status: DocumentStatus;
  page_count: number | null;
  failure_reason: string | null;
  created_at: string;
}

export interface CitationContract {
  id: string;
  document_id: string;
  document_name: string;
  chunk_id: string;
  physical_page: number;
  logical_page: string | null;
  source_text: string;
  bbox: number[] | null;
}

