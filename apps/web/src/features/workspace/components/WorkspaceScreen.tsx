"use client";

import { useEffect, useState } from "react";
import { ChevronLeft, Menu } from "lucide-react";
import Link from "next/link";
import type { Citation, Document, Workspace } from "@/types/api";
import { listDocuments } from "@/features/documents/api/documents";
import { DocumentSidebar } from "@/features/documents/components/DocumentSidebar";
import { PdfViewer } from "@/features/pdf-viewer/components/PdfViewer";
import { ChatPanel } from "@/features/chat/components/ChatPanel";

export function WorkspaceScreen({ workspace }: { workspace: Workspace }) {
  const [documents, setDocuments] = useState<Document[]>([]); const [selected, setSelected] = useState<Document>(); const [page, setPage] = useState(1); const [citation, setCitation] = useState<Citation>();
  useEffect(() => { listDocuments(workspace.id).then(items => { setDocuments(items); setSelected(items.find(item => item.status === "ready") ?? items[0]); }).catch(() => undefined); }, [workspace.id]);
  function selectDocument(document: Document) { setSelected(document); setPage(1); setCitation(undefined); }
  function openCitation(next: Citation) { const document = documents.find(item => item.id === next.document_id); if (document) setSelected(document); setCitation(next); setPage(next.physical_page); }
  return <main className="grid h-screen grid-rows-[58px_1fr] overflow-hidden bg-[var(--paper)]"><header className="flex items-center justify-between border-b border-[var(--line)] bg-white px-4"><div className="flex min-w-0 items-center gap-3"><Link href="/dashboard" className="focus-ring rounded-lg p-1.5 text-[var(--slate)] hover:bg-[#f3f3ef]"><ChevronLeft size={20}/></Link><span className="grid h-7 w-7 place-items-center rounded-lg bg-[var(--navy)] text-xs font-bold text-white">P</span><span className="truncate text-sm font-bold text-[var(--navy)]">{workspace.name}</span></div><div className="flex items-center gap-2 text-xs font-semibold text-[var(--slate)]"><span className="hidden rounded-full bg-[#e8f4ef] px-2 py-1 text-[#218365] sm:block">Local AI · private</span><Menu size={18}/></div></header><div className="grid min-h-0 grid-cols-1 lg:grid-cols-[250px_minmax(0,1fr)_360px]"><div className="hidden min-h-0 lg:block"><DocumentSidebar workspaceId={workspace.id} documents={documents} selectedId={selected?.id} onSelect={selectDocument} onUploaded={document => { setDocuments(old => [document, ...old]); setSelected(document); }}/></div><PdfViewer document={selected} page={page} citation={citation} onPageChange={setPage}/><div className="min-h-0"><ChatPanel workspaceId={workspace.id} documentIds={documents.filter(item => item.status === "ready").map(item => item.id)} onCitation={openCitation}/></div></div></main>;
}

