"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { listWorkspaces } from "@/features/workspace/api/workspaces";
import { WorkspaceScreen } from "@/features/workspace/components/WorkspaceScreen";
import type { Workspace } from "@/types/api";

export default function WorkspacePage() { const { workspaceId } = useParams<{ workspaceId: string }>(); const [workspace, setWorkspace] = useState<Workspace>(); useEffect(() => { listWorkspaces().then(all => setWorkspace(all.find(item => item.id === workspaceId))).catch(() => undefined); }, [workspaceId]); return workspace ? <WorkspaceScreen workspace={workspace}/> : <main className="grid min-h-screen place-items-center bg-[var(--paper)] text-[var(--slate)]">Loading workspace…</main>; }
