"use client";

import { Mic, Square, Waves } from "lucide-react";
import { useVoiceRecorder } from "@/features/voice/hooks/useVoiceRecorder";

export function VoiceButton({ onTranscript }: { onTranscript: (text: string) => void }) {
  const voice = useVoiceRecorder(onTranscript); const listening = voice.state === "listening";
  return <button onClick={listening ? voice.stop : voice.start} disabled={voice.state === "transcribing"} title={listening ? "Stop recording" : "Ask by voice"} className={`focus-ring grid h-11 w-11 place-items-center rounded-xl transition ${listening ? "bg-red-500 text-white shadow-lg shadow-red-200" : "bg-[#fff0e6] text-[var(--orange-deep)] hover:bg-[#ffe4d2]"}`}>{voice.state === "transcribing" ? <Waves className="animate-pulse" size={19}/> : listening ? <Square size={17} fill="currentColor"/> : <Mic size={19}/>}</button>;
}
