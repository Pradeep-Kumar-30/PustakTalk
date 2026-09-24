import { api } from "@/lib/api/client";

export function transcribeAudio(file: Blob) { const data = new FormData(); data.append("audio", file, "question.webm"); return api<{ transcript: string }>("/voice/transcribe", { method: "POST", body: data }); }
export async function getSpeech(text: string, language?: "en" | "hi") { const { apiBaseUrl } = await import("@/config/env"); const response = await fetch(`${apiBaseUrl}/voice/speak`, { method: "POST", credentials: "include", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text, language }) }); if (!response.ok) throw new Error("Speech generation failed"); return response.blob(); }

