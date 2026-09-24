"use client";

import { ChangeEvent, useRef, useState } from "react";
import { FileText, FolderOpen, LoaderCircle, Plus, UploadCloud } from "lucide-react";
import type { Document } from "@/types/api";
import { uploadDocument } from "@/features/documents/api/documents";

export function DocumentSidebar({ workspaceId, documents, selectedId, onSelect, onUploaded }: { workspaceId: string; documents: Document[]; selectedId?: string; onSelect: (document: Document) => void; onUploaded: (document: Document) => void }) {
  const input = useRef<HTMLInputElement>(null);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  async function choose(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]; if (!file) return;
    setUploading(true); setError("");
    try { onUploaded(await uploadDocument(workspaceId, file)); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Upload failed"); }
    finally { setUploading(false); event.target.value = ""; }
  }
  return <aside className="flex min-h-0 flex-col border-r border-[var(--line)] bg-white/75"><div className="flex items-center justify-between p-4"><div><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--slate)]">Library</p><h2 className="mt-1 font-bold text-[var(--navy)]">Your documents</h2></div><button onClick={() => input.current?.click()} className="focus-ring grid h-9 w-9 place-items-center rounded-lg bg-[var(--navy)] text-white" aria-label="Upload PDF"><Plus size={18}/></button><input ref={input} onChange={choose} accept="application/pdf,.pdf" type="file" className="hidden"/></div><div className="mx-3 border-t border-[var(--line)]"/>{error && <p className="m-3 rounded-lg bg-red-50 p-2 text-xs text-red-700">{error}</p>}<div className="min-h-0 flex-1 overflow-y-auto p-2">{documents.length === 0 ? <button onClick={() => input.current?.click()} className="focus-ring m-2 grid w-[calc(100%-1rem)] place-items-center rounded-xl border border-dashed border-[var(--line)] bg-[#fbfaf6] px-4 py-8 text-center"><UploadCloud className="text-[var(--orange)]"/><span className="mt-3 text-sm font-bold text-[var(--navy)]">Drop in your first PDF</span><span className="mt-1 text-xs text-[var(--slate)]">Up to 50 MB</span></button> : documents.map(document => <button key={document.id} onClick={() => onSelect(document)} className={`focus-ring mb-1 flex w-full items-start gap-3 rounded-xl p-3 text-left transition ${selectedId === document.id ? "bg-[#fff0e6]" : "hover:bg-[#f5f5f1]"}`}><span className={`mt-0.5 rounded-lg p-2 ${document.status === "ready" ? "bg-[#e8f4ef] text-[#218365]" : "bg-[#f2f0e9] text-[var(--orange-deep)]"}`}>{document.status === "processing" || document.status === "uploaded" ? <LoaderCircle className="animate-spin" size={16}/> : <FileText size={16}/>}</span><span className="min-w-0"><span className="block truncate text-sm font-semibold text-[var(--navy)]">{document.original_filename}</span><span className="mt-1 block text-xs text-[var(--slate)]">{document.status === "ready" ? `${document.page_count ?? "?"} pages · ready` : document.status}</span></span></button>)}</div><div className="p-3"><button disabled={uploading} onClick={() => input.current?.click()} className="focus-ring flex w-full items-center justify-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm font-bold text-[var(--navy)] hover:bg-[#f9f8f3]"><FolderOpen size={16}/>{uploading ? "Adding PDF…" : "Add a document"}</button></div></aside>;
}

