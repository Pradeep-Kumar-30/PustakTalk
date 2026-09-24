"use client";

import { useRef, useState } from "react";
import { transcribeAudio } from "@/features/voice/api/voice";

export type VoiceState = "idle" | "listening" | "transcribing" | "error";

export function useVoiceRecorder(onTranscript: (text: string) => void) {
  const [state, setState] = useState<VoiceState>("idle");
  const recorder = useRef<MediaRecorder | null>(null); const chunks = useRef<Blob[]>([]);
  async function start() { try { const stream = await navigator.mediaDevices.getUserMedia({ audio: true }); const next = new MediaRecorder(stream); recorder.current = next; chunks.current = []; next.ondataavailable = event => chunks.current.push(event.data); next.onstop = async () => { stream.getTracks().forEach(track => track.stop()); setState("transcribing"); try { const result = await transcribeAudio(new Blob(chunks.current, { type: next.mimeType })); onTranscript(result.transcript); setState("idle"); } catch { setState("error"); } }; next.start(); setState("listening"); } catch { setState("error"); } }
  function stop() { recorder.current?.stop(); }
  return { state, start, stop };
}
