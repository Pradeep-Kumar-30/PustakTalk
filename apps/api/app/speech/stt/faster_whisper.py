import os
import tempfile

from faster_whisper import WhisperModel

from app.speech.stt.base import SpeechToTextProvider


class FasterWhisperProvider(SpeechToTextProvider):
    def __init__(self, model_name: str, device: str, compute_type: str) -> None:
        self._model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio: bytes, filename: str, language: str | None = None) -> str:
        suffix = os.path.splitext(filename)[1] or ".webm"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temporary:
            temporary.write(audio)
            path = temporary.name
        try:
            segments, _ = self._model.transcribe(
                path, language=language, beam_size=5, vad_filter=True
            )
            return " ".join(segment.text.strip() for segment in segments).strip()
        finally:
            os.unlink(path)
