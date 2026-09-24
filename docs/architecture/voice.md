# Voice architecture

```text
microphone → MediaRecorder → /voice/transcribe → faster-whisper
           → /chat → citations + answer → /voice/speak → Piper WAV → browser playback
```

The UI exposes `idle`, `listening`, `transcribing`, and failure states, and pauses active audio before starting a new spoken answer. The browser microphone is only requested after a deliberate user action.

`faster-whisper` uses CTranslate2 and supports CPU `int8` configuration. The TTS adapter executes Piper without a shell and sends text over stdin. Piper's currently active upstream is GPL-3.0, and individual voice model cards can have further restrictions; a production distributor must review both the engine and selected voice licences before shipping.

